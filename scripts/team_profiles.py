#!/usr/bin/env python3
"""Read, refresh, and share the team profiles used by the NBA preview skill."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import re
import subprocess
from tempfile import NamedTemporaryFile, TemporaryDirectory
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "sharpredux/nba-betting-preview"
BRANCH = "refs/heads/main"
TEAM_IDS = frozenset("""
ATL BOS BKN CHA CHI CLE DAL DEN DET GSW HOU IND LAC LAL MEM MIA MIL MIN
NOP NYK OKC ORL PHI PHX POR SAC SAS TOR UTA WAS
""".split())
FRESH_FOR = timedelta(minutes=15)
MAX_BYTES = 12_000
HEADINGS = (
    "## Coaching and rotations",
    "## On-court tendencies",
    "## Competitive posture",
    "## Sources",
)
FRONTMATTER = re.compile(
    r"\A---\nteam: ([A-Z]{3})\nseason: (\d{4}-\d{2})\n"
    r"(?:last_refreshed_at: ([^\n]+)\n)?---\n"
)


def utc_now():
    return datetime.now(timezone.utc)


def profile_path(team):
    return f"teams/{team}/TEAM.md"


def parse_profile(body, team, *, draft=False):
    if len(body.encode("utf-8")) > MAX_BYTES:
        raise ValueError(f"{team} profile is too long")
    match = FRONTMATTER.match(body)
    if not match or match[1] != team or (match[3] is None) != draft:
        raise ValueError(f"{team} profile has invalid frontmatter")
    sections = list(re.finditer(r"^## .+$", body[match.end():], re.MULTILINE))
    if tuple(section[0] for section in sections) != HEADINGS:
        raise ValueError(f"{team} profile is missing the required sections")
    content = body[match.end():]
    if any(not content[section.end():following.start()].strip()
           for section, following in zip(sections, sections[1:])):
        raise ValueError(f"{team} profile has an empty section")
    if not re.search(r"https://[^\s)]+", content[sections[-1].end():]):
        raise ValueError(f"{team} profile requires direct source links")
    timestamp = None if draft else datetime.strptime(
        match[3], "%Y-%m-%dT%H:%M:%SZ"
    ).replace(tzinfo=timezone.utc)
    return match[2], timestamp


def is_fresh(body, team, season, now):
    if body is None:
        return False
    profile_season, refreshed = parse_profile(body, team)
    return profile_season == season and timedelta(0) <= now - refreshed < FRESH_FOR


def accepted_drafts(directory, teams, season, now):
    drafts = {}
    for team in teams:
        body = (directory / f"{team}.md").read_text(encoding="utf-8")
        if parse_profile(body, team, draft=True)[0] != season:
            raise ValueError(f"{team} draft has the wrong season")
        timestamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
        line = f"season: {season}\n"
        drafts[team] = body.replace(line, f"{line}last_refreshed_at: {timestamp}\n", 1)
        parse_profile(drafts[team], team)
    return drafts


def git(repo, *args, input_text=None, index=None):
    env = {key: value for key, value in os.environ.items()
           if key not in {"GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE",
                          "GIT_COMMON_DIR", "GIT_OBJECT_DIRECTORY"}}
    env["GIT_TERMINAL_PROMPT"] = "0"
    if index is not None:
        env["GIT_INDEX_FILE"] = str(index)
    data = input_text.encode("utf-8") if input_text is not None else None
    return subprocess.run(
        ["git", "-C", str(repo), *args], input=data, env=env,
        capture_output=True, check=True, timeout=25,
    ).stdout.decode("utf-8", errors="replace")


def checkout(override):
    candidates = [override] if override else [ROOT, Path.home() / "nba-betting-preview"]
    valid_urls = {
        f"https://github.com/{REPOSITORY}", f"git@github.com:{REPOSITORY}",
        f"ssh://git@github.com/{REPOSITORY}",
    }
    for candidate in candidates:
        repo = candidate.resolve()
        try:
            if Path(git(repo, "rev-parse", "--show-toplevel").strip()).resolve() != repo:
                continue
            urls = []
            for option in ((), ("--push",)):
                urls.extend(git(repo, "remote", "get-url", "--all", *option, "origin").splitlines())
            if urls and all(url.rstrip("/").removesuffix(".git") in valid_urls for url in urls):
                return repo
        except (OSError, subprocess.SubprocessError):
            continue
    return None


@contextmanager
def fetched_head(repo):
    ref = f"refs/nba-betting-preview/{uuid4().hex}"
    try:
        git(repo, "fetch", "--no-tags", "--no-write-fetch-head", "origin", f"{BRANCH}:{ref}")
        yield git(repo, "rev-parse", ref).strip()
    finally:
        try:
            git(repo, "update-ref", "-d", ref)
        except (OSError, subprocess.SubprocessError):
            pass


def validated(body, team):
    parse_profile(body, team)
    return body


def repo_profiles(repo, head, teams, notes):
    profiles = {}
    for team in teams:
        try:
            profiles[team] = validated(git(repo, "show", f"{head}:{profile_path(team)}"), team)
        except (ValueError, OSError, subprocess.SubprocessError):
            notes.append(f"{team} shared profile is missing or invalid.")
    return profiles


def public_profiles(teams, notes):
    from concurrent.futures import ThreadPoolExecutor

    def fetch(team):
        url = (f"https://raw.githubusercontent.com/{REPOSITORY}/main/{profile_path(team)}"
               f"?check={uuid4().hex}")
        try:
            request = Request(url, headers={"Cache-Control": "no-cache"})
            with urlopen(request, timeout=10) as response:
                return team, validated(response.read(MAX_BYTES + 1).decode("utf-8"), team), True
        except HTTPError as error:
            return team, None, error.code == 404
        except ValueError:
            return team, None, True
        except OSError:
            return team, None, False

    profiles, checked = {}, set()
    with ThreadPoolExecutor(max_workers=8) as pool:
        for team, body, reachable in pool.map(fetch, teams):
            if reachable:
                checked.add(team)
            if body is None:
                notes.append(f"{team} shared profile is missing, invalid, or unavailable.")
            else:
                profiles[team] = body
    return profiles, checked


def refresh_commit(repo, head, profiles):
    # Use a private index so unrelated edits and staged files cannot enter the commit.
    with TemporaryDirectory(prefix="nba-profile-index-") as directory:
        index = Path(directory) / "index"
        git(repo, "read-tree", head, index=index)
        for team, body in profiles.items():
            blob = git(repo, "hash-object", "-w", "--stdin", input_text=body).strip()
            git(repo, "update-index", "--add", "--cacheinfo",
                f"100644,{blob},{profile_path(team)}", index=index)
        tree = git(repo, "write-tree", index=index).strip()
        teams = ", ".join(profiles)
        return git(repo, "commit-tree", tree, "-p", head, "-m", f"Refresh NBA team context: {teams}").strip()


def push_refreshed(repo, teams, season, drafts, notes):
    for attempt in range(2):
        with fetched_head(repo) as head:
            profiles = repo_profiles(repo, head, teams, notes)
            # Another collaborator may have refreshed a team since check ran.
            pending = {team: drafts[team] for team in teams if team in drafts
                       and not is_fresh(profiles.get(team), team, season, utc_now())}
            if not pending:
                return head, profiles, set()
            commit = refresh_commit(repo, head, pending)
            try:
                git(repo, "push", "origin", f"{commit}:{BRANCH}")
            except subprocess.CalledProcessError:
                if attempt == 0:
                    with fetched_head(repo) as latest:
                        if latest != head:
                            continue
                raise
            return commit, profiles | pending, set(pending)


def sync_checkout(repo, head, profiles, notes):
    if not profiles:
        return
    try:
        if all(read_local(repo, team) == body for team, body in profiles.items()):
            return
        if git(repo, "status", "--porcelain") or git(repo, "symbolic-ref", "HEAD").strip() != BRANCH:
            notes.append("Repository checkout has local changes or is off main. Shared profiles were read directly.")
            return
        git(repo, "merge-base", "--is-ancestor", "HEAD", head)
        changes = git(repo, "diff", "--name-only", "HEAD", head).splitlines()
        if any(not re.fullmatch(r"teams/[A-Z]{3}/TEAM\.md", path) for path in changes):
            notes.append("Repository checkout also has incoming skill changes. Update its main branch separately.")
            return
        git(repo, "merge", "--ff-only", head)
    except (OSError, subprocess.SubprocessError):
        notes.append("Could not fast-forward the repository checkout. The shared profile is still available.")


def read_local(root, team):
    try:
        return validated((root / profile_path(team)).read_text(encoding="utf-8"), team)
    except (OSError, ValueError):
        return None


def mirror(root, team, body):
    path = root / profile_path(team)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError("Profile path leaves the installed skill")
    if read_local(root, team) == body:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                            dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            handle.write(body)
            handle.close()
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def run(args):
    notes = []
    override = os.environ.get("NBA_BETTING_PREVIEW_REPO_ROOT")
    repo = checkout(Path(override).expanduser() if override else None)
    now = utc_now()
    teams = tuple(dict.fromkeys(args.teams))
    drafts = accepted_drafts(args.draft_dir, teams, args.season, now) if args.command == "apply" else {}
    shared, checked, published = {}, set(), set()
    shared_commit = None
    if repo:
        try:
            if drafts:
                shared_commit, shared, published = push_refreshed(repo, teams, args.season, drafts, notes)
            else:
                with fetched_head(repo) as head:
                    shared_commit = head
                    shared = repo_profiles(repo, head, teams, notes)
            checked = set(teams)
            if not args.historical:
                sync_checkout(repo, shared_commit, shared, notes)
        except (OSError, subprocess.SubprocessError) as error:
            detail = (getattr(error, "stderr", None) or b"").decode("utf-8", errors="replace").splitlines()
            reason = detail[-1] if detail else type(error).__name__
            notes.append(f"GitHub refresh check or publish failed ({reason}).")
    elif drafts:
        notes.append("Publishing requires a writable clone with the project's origin and GitHub collaborator credentials.")
    if not checked:
        shared, checked = public_profiles(teams, notes)

    result = {}
    now = utc_now()
    # A Git checkout must stay clean for its owner. A copied install has its own mirror.
    standalone = not (ROOT / ".git").exists()
    for team in teams:
        local = read_local(ROOT, team)
        body = shared.get(team)
        if args.historical:
            body = body or local
            state = "historical_check"
        elif team in published:
            state = "published"
        elif is_fresh(body, team, args.season, now):
            state = "shared_fresh"
        elif team in drafts:
            state, body = "local_only", drafts[team]
        elif team not in checked and is_fresh(local, team, args.season, now):
            state, body = "local_only", local
        else:
            state, body = "refresh_required", body or local

        if standalone and body is not None and state in {"published", "shared_fresh", "local_only"}:
            try:
                mirror(ROOT, team, body)
            except (OSError, ValueError):
                notes.append(f"Could not sync {team} to the installed skill.")
        result[team] = {"state": state, "profile": body}
    return {"teams": result, "shared_commit": shared_commit, "notes": list(dict.fromkeys(notes))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(required=True, dest="command")
    for command in ("check", "apply"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--season", required=True, help="NBA season, such as 2026-27")
        sub.add_argument("teams", nargs="+", choices=sorted(TEAM_IDS))
        if command == "check":
            sub.add_argument("--historical", action="store_true")
        else:
            sub.set_defaults(historical=False)
            sub.add_argument("--draft-dir", required=True, type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r"\d{4}-\d{2}", args.season):
        parser.error("--season must have YYYY-YY format")
    try:
        print(json.dumps(run(args), ensure_ascii=False, indent=2))
    except (ValueError, OSError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
