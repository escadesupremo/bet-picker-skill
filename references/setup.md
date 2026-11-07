# Setup

Setup turns the user's way of picking bets into their rules file. The rules are theirs: write down what they say, in their words, and don't add, improve or judge anything. A good rules file is short, specific and in the user's voice. Every number they give goes in the settings block; everything else goes under the headings, in their words.

## 1. Offer three ways to start
If a rules file is already in use, say where it is and ask whether to change it or start again. Never overwrite it without a yes. Before you replace it, copy it to `rules.backup.md` in the same folder.

Otherwise, introduce the skill and offer the ways to start in a few short lines, then stop until the user answers:

> This skill finds the football and NFL games that fit your own betting rules, for your singles or parlays. First I need your rules. How do you want to start?
> 1. Answer a few short questions (about 5 minutes)
> 2. Start from an example rule set and change what doesn't fit
> 3. Paste notes you already have

## 2a. Questions
Ask one topic at a time, in this order, and wait for each answer. Keep each question to a line or two, with a short example answer so the user knows what you mean. Skip a topic an earlier answer makes irrelevant, e.g. the NFL question for someone who only bets football. If an answer is vague where it matters ("good odds"), ask once for the number; if they don't have one, keep their words and leave the setting out.

| # | Ask | Example answer | Fills |
|---|---|---|---|
| 1 | **Sports:** football, the NFL, or both? | "Both" | `sports` |
| 2 | **Odds per pick:** the lowest and highest odds you'd take on one game, and how strict is that? Any league where it's different? | "1.30 to 1.80, rarely outside. In Germany only from 1.40." | `odds` (`min`, `max`, `hedge`, `by_league`) |
| 3 | **Singles or parlays:** how many games together, and what total odds? | "2 or 3 games, total 1.80 to 3" | `parlay` |
| 4 | **Leagues and teams:** which leagues, which teams in each, and against what kind of opponent? | "Premier League: Arsenal or City against a bottom-half team. Serie A: Inter at home only." | Team list, `roles`, Leagues, Where to look |
| 5 | **Form:** do you check recent form? How many games, and what counts as good form? If they play the NFL, ask whether it applies there too. | "Last 5, at least 2 wins and at most 2 losses" | `form` (`sports` only if the NFL too) |
| 6 | **When you drop a game:** what makes you skip a game that otherwise fits? Ask about European games a few days before, and whether some teams are exempt. | "Teams close in the table. My team played in Europe less than 4 days before, except PSG." | `european_gap`, When I drop a game |
| 7 | **Close calls:** when a game with one of your teams could go either way on a judgement call, should it go in, marked "Marginal", or stay out? | "In, if it's one of my teams" | Marginal calls |
| 8 | **Cups, Europe and internationals:** do you play them? What makes one worth it? | "FA Cup ties between teams two divisions apart" | Cups, Champions League…, Internationals, Where to look |
| 9 | **NFL** (if they play it): what do you look for, and at what odds? | "Against a team starting a backup QB, 1.30 to 1.60" | NFL, `odds.nfl` |
| 10 | **Settings:** decimal or American odds? Should each run end with what it cost in tokens? Offer the defaults (decimal, yes) so they can just say "defaults". | "Defaults" | `odds_format`, `show_cost` |

How the answers become the file:
- **Teams.** Each team the user names becomes a Team list row: league, team, role, and their note ("possibly", "sometimes"). The role is `Pick` unless they describe another kind, e.g. a team they back only in some games, or opponents they look for ("clear relegation teams"). Then add a role with a short name and their meaning to `roles`. The league terms ("against a bottom-half team") go under Leagues, in their words.
- **Form, gaps, odds.** "Last 5" is `form.last: 5`; "at least 2 wins" is `min_wins: 2`; "less than 4 days" and "3 days or less" are both `european_gap.min_days: 4`; a European game after the league game counting too is `counts: both`. If they name only some European competitions ("Champions League or Europa League"), list those in `competitions`. A team that never drops for a European game goes in `exempt`.
- **Hedges.** Keep the user's word for how strict a rule is ("rarely", "usually") in the setting's `hedge`, or in the rule's words.
- **Where to look.** Write it yourself from their answers: which leagues, cups and competitions to search, and for which teams.

## 2b. Start from an example
List the files in `examples/` with a one-line summary of each (the line under its title), and ask which one is closest. Copy it to the rules file, show it, and ask what to change. Make each change the user asks for, in their words.

## 2c. Paste notes
Take what they paste and sort it into the file: numbers into the settings, everything else under the template's headings, in their words, and their teams into the Team list. Then ask the questions above only for the topics their notes don't cover.

## 3. Ask about what's unclear
Before writing the file, look for anything that would change which games pass and that could be read two ways. For example:
- "Last 5 games": all competitions, or the league only?
- "3 days after a European game": does a European game after this one count too?
- "A weaker team": weaker by table position, odds or division?

Ask about up to 3 of these, the ones that matter most, in one short message. Record the answers under **Clarifications**. Leave anything else for the screening to flag game by game.

## 4. Write the file
Write it to the rules file in use if the user chose to replace it, to the path they named if they named one, and otherwise to `~/.bet-picker/rules.md` (on Windows, `%USERPROFILE%\.bet-picker\rules.md`), creating the folder if needed.

Lay it out like `rules-template.md`:
- **Settings:** only the settings SKILL.md describes, with the user's values. Leave out any they don't use (e.g. no `form` if they don't check form). Keep a short comment on a setting where it helps.
- **Rules:** each rule as a short bullet in the user's words, under one heading. Write "None" under a heading the user doesn't play. Remove the template's HTML comments.
- **Team list:** one table row per team, every role defined in `roles`.

Then run `python scripts/check_rules.py <path>` from this skill's base directory. If it lists problems, fix the file and run it again. If it can't run (no PyYAML), read the settings block back yourself and check each value against SKILL.md.

Then:
- Show the file path and the rules.
- Tell the user they can change any rule by just telling you, e.g. "add Celtic to my teams" or "make the odds 1.25 to 1.80".

## 5. Carry on
If the user's first message gave a date range or listed games, start the workflow with it now. Otherwise ask for the range as in step 1 of the workflow.
