# bet-picker

A [Claude Code](https://claude.com/claude-code) skill that finds the bets that fit your own rules: football (soccer) and NFL winner bets, for singles or parlays.

You tell it once how you pick bets: odds ranges, leagues and teams, when you drop a game. After that, give it a date range. It finds the fixtures and odds on the web, screens them against your rules, researches what your rules ask about (tables, form, games around European fixtures, quarterback injuries), and returns every game that passes in one table:

| Game | Description | Pick | Odds | Date |
|---|---|---|---|---|
| Venezia v Inter | Serie A. Inter 1st, Venezia bottom. Last 5: Inter 4W 1D 0L, Venezia 1W 0D 4L. | Inter | 1.36 | Wed 28 Oct |
| Eagles v Cowboys | NFL. Jalen Hurts is out for the season, so backup Tanner McKee starts. | Cowboys | 1.46 | Mon 26 Oct |

Under the table, one sentence gives the tokens the run used and what they would cost at Anthropic API rates. You can turn it off.

## Install

Copy this folder into your Claude Code skills directory as `bet-picker`, and install the two Python packages its scripts use:

```
git clone https://github.com/escadesupremo/bet-picker-skill ~/.claude/skills/bet-picker
pip install pyyaml openpyxl
```

`pyyaml` checks your rules file; `openpyxl` is only needed if you keep your teams in an Excel sheet.

## Set up your rules

In Claude Code, run `/bet-picker`. The first time, it asks how you want to start:

1. **Answer a few short questions**: sports, odds, singles or parlays, leagues and teams, form, when you drop a game, close calls, cups and Europe, the NFL.
2. **Start from an example** in [examples/](examples/) and change what doesn't fit.
3. **Paste notes** you already have.

It writes your rules to `~/.bet-picker/rules.md`, outside the skill folder, so updating the skill never touches them. The file is plain Markdown, laid out like [rules-template.md](rules-template.md):
- **A settings block** at the top holds every rule with a number or a list: the odds range (and other ranges for some leagues or the NFL), singles or parlays, the form test, the gap after a European game and the teams exempt from it, and the roles a team can have. These are hard rules: a game that breaks one never makes the table.
- **Your rules** follow, in your own words: your team list, the terms for each league, when you drop a game, close calls, cups, Europe, internationals, the NFL, where to look, and **Clarifications** on how to read rules that could mean two things.

Edit the file yourself, or tell Claude: "add Celtic to my teams", "make the odds 1.25 to 1.80", "I never back away teams", "show my rules". Each change is checked with `scripts/check_rules.py`. To start over, say "set up my rules again".

[SKILL.md](SKILL.md) is the engine: how to find, screen and research games, and what each setting means. It holds no rules of its own.

## Use

Ask something like "what can I play this weekend?" or run `/bet-picker`. If you don't give dates, it asks for them first. You can also paste in games with odds, table positions and form, and it checks them against your rules using your numbers.

Odds come from public comparison sites and move constantly. Always check the price at your own bookmaker.

## What's in here

| File | What it is |
|---|---|
| `SKILL.md` | The engine: setup, rule changes, the settings, and the screening steps |
| `rules-template.md` | The layout of a rules file |
| `examples/` | Rule sets to start from |
| `references/setup.md` | The setup questions, and how the answers become the file |
| `references/sources.md` | Which websites work for odds, tables, results and injuries |
| `scripts/check_rules.py` | Checks a rules file |
| `scripts/teams.py` | Reads a team sheet |
| `scripts/run_cost.py` | Measures the tokens and cost of a run from the session transcript |
| `evals/` | Test cases |

## Tests

Each case in `evals/` has a prompt, a rules file where it needs one, and the checks a good answer must pass. With Claude Code you can run them from this folder:

```
claude plugin eval . --scaffold --allow-tools Write Edit Bash
```

On Windows the eval runner can't sandbox the shell, which the skill needs for its scripts, so run the cases there by hand.

## Disclaimer

This applies your rules; it doesn't predict results, and no game it lists is a sure thing. Bet only what you can afford to lose.
