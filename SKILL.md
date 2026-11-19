---
name: nba-betting-preview
description: "Analyze a specific NBA matchup for predictions or betting research using current sourced odds, injuries, rest, travel, scoring, and team/player form. Automatically use when the user asks about an NBA game, matchup, pick, prediction, spread, total, or moneyline. Cover only the named or contextually identified game; scan the full slate only when explicitly requested."
---

# NBA Betting Preview

Produce a compact, evidence-based preview for every requested game. Use basketball judgment to weigh the evidence against the available price. Treat missing information and a pass as valid outcomes.

## Defaults and invocation

- Use this skill automatically for requests to preview, predict, or assess betting markets for an NBA game, even when the user does not invoke the skill by name.
- A named or contextually clear matchup means **that game only**. Do not add other games, a slate summary, or unrelated picks. Cover multiple games only when the user explicitly asks for a slate, all games, or multiple named matchups.
- If the user asks about a game but neither the prompt nor conversation context identifies the matchup, ask which game they mean. A bare `$nba-betting-preview` invocation or date-only request does not imply a full-slate request.
- For a named matchup with no date, resolve its next scheduled meeting and state the date. Use **Asia/Manila** unless the user specifies another timezone.
- The local date means tipoffs within local midnight to the following midnight. For an explicit slate request, fetch all NBA/ET schedule dates that intersect that interval, then filter by actual tipoff timestamps. Do not equate a Philippine date with the NBA's ET game date.
- For each requested game, label started, final, postponed, or canceled status and give pregame recommendations only if it is still scheduled to start. If none of the requested games remain upcoming, say so without silently moving to tomorrow.
- Evaluate full-game spread, total, and moneyline. Default to current public consensus context with named sources. Explicit user lines or a requested sportsbook take precedence and retain their as-of time. Player props require a separate request.
- Lead with the quick scan below for the requested game or games. Expand a matchup when requested or when a material exception needs explanation. For a comprehensive report on a specific game, use the report-readiness check below. Do not suggest stakes or bankroll allocation.

## Research workflow

Read [the research guide](references/research.md) before collecting a slate. Use available browsing or sports tools to obtain current facts; memory and search snippets alone cannot establish current lines or player availability. No paid feed or API key is required. If browsing is unavailable, provide a clearly limited framework or analyze supplied data with its limitations; do not present it as a current slate scan.

### Targeted crawling when information is incomplete or uncertain

Search results are discovery leads, not verification. When a required field is missing, stale, internally inconsistent, or consequentially uncertain, continue by opening and inspecting the underlying source page, report, schedule, game log, or odds board. Search specifically for the matchup/team, relevant date, and field in question; follow useful links to primary or more direct sources, and check newer updates where timing matters. Do not mark a field verified from a search snippet alone.

- For rest and travel, inspect each team's recent game log or schedule across at least the previous six NBA/ET dates. Confirm the last actual game, its venue, the next venue, days off, and schedule density before calculating miles. Do not infer a previous venue from the team's home city or a B2B from a generic slate summary.
- For injuries, open the newest applicable official report and inspect the matchup's entries; then check later team announcements or credible, named reporting for changes to availability or minutes. Preserve issue/observation times and conflicts. A report that is pending, missing, or not yet submitted stays unresolved until a source establishes the status.
- For odds, inspect the actual matchup row on a current odds board or sportsbook page. Capture the market period, selection, number, price/juice, provider, and observation time. Cross-check another accessible source when possible; distinguish current quotes from openers and stale snapshots.
- For scoring and statistics, inspect a current-season team-stat table and verify the season, regular-season/postseason scope, games played, and cutoff date. Do not fill missing PPG from memory or from a differently dated source without labeling it.
- If the first source is blocked, incomplete, or gives only a snippet, try another direct source instead of repeating the same failed fetch. Continue targeted research for material gaps before drafting. If evidence remains unavailable or sources conflict, state exactly what is unresolved and pass on any conclusion that depends on it; do not manufacture a completion.

### Required team profile check

On every invocation, as soon as the requested matchup or slate is resolved, follow [the team profile workflow](references/team-profiles.md). Check shared freshness, read the profiles for every team in the requested games, and refresh and attempt to publish only stale or missing profiles. Use the 15-minute window per team. Reuse the game logs and other sources already needed for the preview. Read the resulting profiles before ranking any picks. If a profile cannot be read or refreshed, disclose the gap and pass on any angle that depends on it.

### Matchup analysis

1. Establish the requested matchup(s), date, timezone, current time, season, game IDs, venues, tipoffs, and game status. Verify the schedule row for each requested game; reconcile the full schedule only for an explicit slate request.
2. Batch shared sources for the requested game(s): schedule and recent team game logs, the latest applicable official injury report, team statistics, and the odds board. Keep a working record per game of both teams, rest/B2B, previous venues, miles, injuries, markets/prices, PPG, other relevant factors, source links, and source/observation times. Mark unavailable fields explicitly.
3. For **each team**, verify its previous actual game and recent schedule. Show back-to-back status and days off; check 3-in-4 or 4-in-6 stretches, recent overtime, and large timezone changes when relevant. Use NBA/ET game dates for schedule density. Compute approximate miles from the previous game venue to the current venue; label the route and estimate. See the calculation helpers below.
4. Verify player statuses for this matchup and report issue time. Explain important absences through role, expected minutes, replacement quality, and lineup effects. Separate confirmed facts from expectations. For a material questionable player, show how the view changes if in or out; hold the affected recommendation when that uncertainty could reverse it.
5. Record current spread, total, and moneyline with the **price/juice**, market period, bookmaker or aggregator, and observation time. Cross-check consensus where possible and retain material ranges. Read [the edge guide](references/edges.md) before assigning ratings or ranking bets.
6. Collect both teams' current-season PPG and games played, plus points allowed, pace, and offensive/defensive efficiency where accessible. Assess team and relevant-player momentum/recent form against season baselines using verified samples, role and lineup context, opponent quality, venue, and schedule. Consider home/away splits, matchup strengths, rest, and home court when material. Label sample windows and missing data; PPG alone does not establish a fair total. Follow the momentum guidance in [the research guide](references/research.md#basketball-context).
7. Compare the basketball case with the actual quoted market. Weigh relevant coaching, tendencies, and goals from the team profiles alongside current evidence. Count overlapping evidence once. Record supporting evidence, the strongest counterargument, and what could invalidate the angle. Refresh the injury and market sources for shortlisted recommendations immediately before presenting them. If new information changes a line or premise, reassess rather than keeping the earlier rating.

## First response

Open with the selected local date/timezone and analysis time. Present one compact row or short card per requested game, in tipoff order, with these fields. For a single-game request, include only that matchup:

| Field | Required content |
| --- | --- |
| Matchup / tip | Away at home, local tip time, status if not upcoming. |
| B2B / rest | Both teams, clearly identified; days off and notable schedule density. |
| Travel miles | Both teams, approximate venue-to-venue miles; use `unknown` where unverified. |
| Injury report | Material players and reported statuses; report issue time and unresolved key news. |
| Spread / O-U / ML | Explicit team/side, number and price; source and observation time. |
| PPG | Both teams' current-season PPG; season/sample context. |
| Best angle | One best supported market or pass, qualitative tier, short reason, and key risk. |

Put the six requested surface factors—B2B, miles, injuries, spread, total, and edge—where they can be scanned without reading a long breakdown. Keep shared source/timestamp legends concise, but make each fact traceable to a direct link. Never hide missing games or fields to make the board look complete.

After the board, rank only supported candidates. For each give the quoted selection and price, tier, brief supporting case, strongest counterargument, and unresolved trigger that would change it. A lean is a watchlist item. If no angle clears the evidence requirements, say **“No supported betting edge on this snapshot.”** Being best on the slate alone does not justify a bet. End with only the material news or line changes to recheck.

Use **Pass / Lean / Moderate / Strong** as qualitative evidence tiers, never as win-rate estimates. Avoid guarantees, fabricated model projections, and numerical EV or probability claims without a separately supplied, validated model. Do not assume the consensus quote is available at the user's book.

## Comprehensive report for a specific game

When the user requests a comprehensive, full, or detailed report for a named matchup, begin with **“Report timing: Proceed now”** or **“Report timing: Wait for injury clarity.”** Read [the injury timing guidance](references/research.md#injury-timing-and-report-readiness) and explain whether waiting for later injury news would materially improve the report. Include the latest report's issue time, the current analysis time, and time to tipoff in Asia/Manila (or the user's requested timezone).

- **Proceed now:** Current, verified availability information supports a useful comprehensive assessment, and remaining injury uncertainty is unlikely to reverse the market conclusions. Identify any minor unresolved status without automatically delaying the report. This means the report is ready; the betting conclusion can still be pass.
- **Wait for injury clarity:** A missing, outdated, conflicting, or unresolved availability/minutes update could materially change the preferred side, total, moneyline value, or strength of the conclusion. Name the player(s), the missing fact, the affected market(s), and how the in/out or restricted/unrestricted scenarios change the analysis. Label the current report **provisional**, and hold the affected betting call. An unaffected market may still be assessed on its own evidence.

Provide the available comprehensive analysis in the current response even when recommending a wait. Include the material findings from both team profiles and how they affect the market comparison. Finish with the exact update needed and the next useful recheck trigger; give an announcement time only if sourced, otherwise say the timing is unconfirmed. Do not invent a universal “final injury report” deadline, treat the latest report as a guarantee against late changes, or automatically wait/poll in the background. Once material news arrives, refresh both availability and market prices before finalizing the conclusion; an earlier quote may no longer apply.

## Calculation helpers

Run these from this skill's directory, or resolve the script path relative to it. They use Python's standard library, have no network access, and do not predict outcomes.

```bash
python3 scripts/context.py window --date 2026-11-11 --timezone Asia/Manila
python3 scripts/context.py miles --origin 0 0 --destination 0 1
```

`window` returns the local interval, UTC boundaries, and the ET dates to query. Omit `--date` to use today's date in the chosen timezone. Filter games with `start_utc <= tipoff_utc < end_utc_exclusive`. `miles` accepts two **latitude longitude** pairs in degrees and returns great-circle miles; the coordinates above are a mathematical example, not NBA venues. Source real venue coordinates before using it. Round displayed miles to roughly the nearest ten and label them approximate. See the research guide for travel assumptions and fallback behavior.
