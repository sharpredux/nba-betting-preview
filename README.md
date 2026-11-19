# NBA Betting Preview

A portable Agent Skill for sourced NBA game predictions and betting previews. It covers the full-game spread, total, and moneyline, with schedule/rest, approximate travel, injuries, scoring context, and qualitative betting edges. A named matchup is the default scope; the skill scans a full slate only when explicitly requested.

## Install

This repository contains one skill at its root. Clone it, then place the complete `nba-betting-preview` folder in the personal skills directory documented by your coding agent:

```sh
git clone https://github.com/sharpredux/nba-betting-preview.git
```

For Codex, you can ask `$skill-installer` to install the skill from this GitHub repository, or copy the cloned folder into a Codex skills directory. Other agents may use a different directory or installation flow; check that agent’s Agent Skills documentation. The package follows the open `SKILL.md` Agent Skills format, but compatibility and discovery depend on the host agent.

After installation, Codex can select the skill automatically for NBA matchup prediction and betting questions, or you can invoke it with `$nba-betting-preview`. It analyzes only the named or contextually clear game; ask for a full slate when you want all games. In other compatible agents, ask for the `nba-betting-preview` skill by name.

## Requirements and limits

- Current slate previews require an agent with live web research that can inspect source pages and reports. Without it, the skill should provide only a limited framework or analyze supplied information.
- The bundled `scripts/context.py` uses Python 3’s standard library to calculate date windows and approximate great-circle miles. It does not fetch data or predict outcomes.
- No paid data feed or API key is required by this skill.
- `agents/openai.yaml` provides optional Codex-specific display metadata; other agents can ignore it.

## Contents

- `SKILL.md` — invocation metadata and preview workflow
- `references/research.md` — source and research guidance
- `references/edges.md` — market comparison and qualitative tier guidance
- `scripts/context.py` — timezone window and distance helpers
- `agents/openai.yaml` — optional Codex UI metadata

## License

MIT. See [LICENSE](LICENSE).
