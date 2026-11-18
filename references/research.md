# Research sources and interpretation

## Source order and efficient collection

Use sources for facts they actually support. Browse the underlying page or report, verify its date and matchup, and link directly to it. An aggregator quoting the same feed as another page is not independent corroboration.

| Information | Preferred source | Fallback and limitations |
| --- | --- | --- |
| Schedule, venues, prior games, status | [NBA schedule](https://www.nba.com/schedule), team schedules, official box scores | A current sports schedule tool or established scoreboard such as ESPN. Reconcile timezones and postponements. |
| Player availability | Current-season injury-report hub at [NBA Official](https://official.nba.com/); open its newest applicable report | Official team communications; then named, reliable reporters for newer news. An older league PDF does not override a verified later team update. Preserve times and identify conflicting reports. |
| PPG and efficiency | [NBA traditional team stats](https://www.nba.com/stats/teams/traditional), [advanced team stats](https://www.nba.com/stats/teams/advanced) | ESPN team stats or Basketball Reference with a verified season, season type, and cutoff. See the [NBA glossary](https://www.nba.com/stats/help/glossary) for metric definitions. |
| Market quotes | Accessible odds comparison board, such as [Covers NBA odds](https://www.covers.com/sport/basketball/nba/odds) or [Oddschecker NBA](https://www.oddschecker.com/us/basketball/nba), showing actual bookmaker quotes | A named sportsbook or established scoreboard with an identified odds provider. A single provider is a sourced snapshot, not verified consensus. |
| Arena coordinates | Official venue information plus an identifiable mapping/geographic source | Verified city coordinates can support a less precise city-to-city estimate, labeled as such. Never invent coordinates. |

Discover the injury hub for the **requested season** instead of hardcoding a season URL. Team reports may not yet have been submitted, especially for the second game of a back-to-back. “Not yet submitted” and “not verified” are different from “no injuries.” Read PDFs when necessary; use page images if extracted rows lose team/player associations.

Collect common schedule, injury, stats, and market pages once for the slate, then research exceptions. Avoid repeated retries of a blocked provider: use another accessible source and disclose the gap. Do not install plugins, subscribe to a feed, or require an API key to complete a normal scan.

## Time, freshness, and missing data

- Default calendar: Asia/Manila. Explicit timezone/date instructions override it. For “tomorrow,” add a local calendar day. Treat explicit NBA/ET dates as ET, and still display converted local tip times.
- Determine the correct season and season type from the schedule. Keep preseason, regular season, and playoffs distinct. Verify the date scope and filters even when a stats page defaults to another period.
- Store an observation time for each source batch and the published/updated time when available. A newly opened page can contain old data. Write “observed at” if no update time is given; do not label it real-time.
- Open the latest applicable injury report for the game date and check newer team news. Report status and report time together. Do not convert questionable, doubtful, probable, or projected starter into confirmed in/out.
- Refresh shortlisted angles' odds and relevant player news at the end of the analysis. If freshness or matchup identity cannot be established, mark the affected field unverified and pass on a recommendation that depends on it. Keep useful analysis of other games.
- A future game's markets or reports may not exist yet. Show them as pending without carrying over an earlier matchup's prices or injuries.
- For a historical date, use a demonstrable pregame cutoff. If archived pregame facts are unavailable, state that a trustworthy pregame reconstruction is unavailable; don't use the result or later news to manufacture an edge.
- When a game is underway or final, retain its row and status but omit a new pregame pick. Postponed or canceled games get no actionable market recommendation.

## Injury timing and report readiness

For a comprehensive report on a specific game, explicitly decide whether to proceed now or wait for material injury clarity. Check the latest official report for both teams, newer official team updates, and credible sourced availability or minutes news. Distinguish a submitted report from a confirmed decision on a player. The league's [injury-report hub](https://official.nba.com/) is the starting point; verify current reporting guidance before quoting submission deadlines. Reports can be updated throughout the day, so a published report or a reporting deadline does not establish an immutable “final” status.

Make the timing decision from the effect of uncertainty on this game's analysis, not merely the presence of a questionable label or the clock:

- **Wait** when an important player's unresolved participation or minutes restriction could reverse the selection or materially change its value/tier; when plausible replacement lineups change the matchup; or when a missing, stale, or conflicting report prevents that assessment. Explain the in/out or minutes scenarios and identify the specific market affected. A back-to-back team's report not yet submitted is a reason to seek clarity, not evidence of a healthy roster.
- **Proceed** when material statuses and restrictions are verified, or remaining uncertainty concerns a role unlikely to change the conclusion. Explain why the unresolved item is immaterial rather than claiming full certainty. Confirmed absences already reflected in the matchup do not by themselves justify waiting.
- Give current local time, report issue time, verified tipoff time, and time remaining. Recommend the next meaningful event to recheck, such as an official availability decision, minutes-limit announcement, or relevant lineup confirmation. Use a stated announcement time only when sourced; otherwise identify the event without inventing a deadline. Near tipoff, unresolved material news still calls for a conditional report or pass.
- Separate **report readiness** from **bet timing**. Proceeding with the report does not imply a profitable wager or an instruction to bet immediately. Waiting for news can change the available number or price; explain that tradeoff without claiming a predictable line move or manufacturing urgency to bet before an update.

Deliver the requested report with its current limitations. If waiting is advised, label it provisional, preserve useful verified context, show conditional scenarios, and defer the affected final betting call. On a later refresh, reprice the selection using current odds and revise the tier as needed; do not reuse stale prices. Do not promise an automatic follow-up or background monitoring.

## Rest and travel

Look back through at least the previous six NBA/ET schedule dates for each team, extending further to locate the last actual game. Use actual played games, not postponed schedule entries. A back-to-back means games on consecutive NBA/ET game dates; same-day rescheduling is a separate exception to flag. Days off are the number of intervening NBA/ET calendar dates. A 3-in-4 or 4-in-6 includes the upcoming game.

For each team, retain the previous game date and venue, then the upcoming venue. Calculate great-circle distance from the **previous venue**, not the team's home city. Both teams may have traveled, including the nominal home team. Same-venue games have approximately zero venue-to-venue miles. Distinct venues in the same metro can have a small distance; a neutral or international game uses its actual venue.

Call this an **approximate previous-venue-to-game-venue distance**. It is not flight mileage or a confirmed itinerary. Days off may allow a return home or another route; disclose that uncertainty when material. At a season opener or after a long break, mark the recent travel leg unknown if only a remote prior game is available. The default quick scan uses the latest leg consistently for both teams, not cumulative season travel. Verify any optional cumulative window separately.

Use `scripts/context.py miles` with sourced coordinates. If execution is unavailable, a sourced distance estimate with its method is acceptable. If the prior venue or coordinates cannot be verified, report unknown; never make up an exact distance. Timezone displacement, direction of travel, rest, altitude, and recent playing load can qualify the estimate. Do not assign a fixed point penalty per mile or treat travel as proof of fatigue.

## Basketball context

Use current-season team PPG and games played as the common scoring reference. Supplement with opponent points allowed, pace, offensive rating, defensive rating, and net rating where available. Recent form usually means the last ten games, or all available games if fewer; identify the sample. Make home/away and lineup splits explicit when they materially affect the comparison.

Use the season as the baseline and recent form as context; account for changes in opponent strength, personnel, and shooting variance. Early-season data is limited. If last season is useful, label it separately and explain roster changes rather than silently blending samples. Never substitute points per 100 possessions for PPG.

For injuries, focus on creation, ball handling, rim protection, spacing, usage, minutes restrictions, and replacement depth. Long-term absences may already be reflected in the season baseline and market. Avoid adjusting twice for the same absence or assigning invented point values. Confirm lineup/rotation changes before treating them as facts.

Relevant matchup factors can include shot profile, three-point volume/variance, rim pressure, rebounding, turnovers, free throws, bench depth, and expected pace. Recent overtime and compressed schedules can increase uncertainty. Give head-to-head results and ATS streaks limited weight when personnel, venue, or sample differs. Motivation, revenge, “must win,” and public/sharp money narratives require specific evidence and cannot establish an edge on their own.
