---
# Settings: every rule with a number or a list. These are hard rules: a game that breaks one is
# dropped. Leave out a setting you don't use; SKILL.md describes each one.

sports: [football, nfl]      # football, nfl, or both
draws: false                 # true if you also back draws
odds_format: decimal         # decimal or american
show_cost: true              # end each run with its tokens and their API cost

odds:
  min: 1.30                  # the lowest odds you'd take on one game
  max: 1.80                  # the highest
  hedge: rarely              # how strict the range is, in your word: never, rarely, usually...
  by_league:                 # optional: other bounds for league games in some leagues
    Germany: {min: 1.40}
  nfl: {min: 1.30, max: 1.60}   # optional: a range of its own for the NFL

parlay:
  legs: [2, 3]               # how many games you combine; [1] for singles
  total_odds: [1.80, 3.00]

form:                        # optional: drop a game when your pick isn't in form
  last: 5                    # how many games
  competitions: all          # all, or league
  min_wins: 2
  max_losses: 2
  team: pick
  # sports: [football, nfl]  # optional: football only without it

european_gap:                # optional: drop a game after a European game
  min_days: 4                # fewer days than this between them drops the game
  counts: before             # before, or both (a European game after it counts too)
  games: league              # league games only
  # competitions: [Champions League, Europa League]   # optional: which count; all three without it
  exempt: []                 # teams that never drop for this

roles:                       # what a team can be in your team list, in your words
  Pick: a team I back against weaker teams, on its league's terms

# teams: teams.xlsx          # optional: a team sheet instead of the Team list table below
---

# My betting rules

<!-- One line on how you bet, e.g. "Big favourites at home, in 2-game parlays." -->

## Ground rules
<!-- Anything that applies to every game, e.g. "Winner only, never a draw", "Never an away team". -->

## Team list
<!-- One row per team you back, or name as an opponent. Role: one of the roles in the settings. -->
| League | Team | Role | Note |
|---|---|---|---|

## Leagues
<!-- For each league, which of your teams you back and against what kind of opponent,
     e.g. "Premier League: Arsenal or City against a bottom-half team." -->

## When I drop a game
<!-- What makes you skip a game that otherwise fits, beyond the settings,
     e.g. "the teams are close in the table, e.g. 2nd v 6th". -->

## Marginal calls
<!-- Whether a game with one of your teams that could go either way on a judgement call goes in,
     marked "Marginal:". Write "None" to leave them out. -->

## Cups
<!-- Domestic cups: which, and what makes a tie worth it. -->

## Champions League, Europa League and Conference League
<!-- Which games, if any. -->

## Internationals
<!-- National-team games: which, if any. -->

## NFL
<!-- What you look for, e.g. "against a team starting a backup QB". -->

## Where to look
<!-- Which fixtures to search, e.g. "Premier League and La Liga games of my teams; FA Cup ties". -->

## Clarifications
<!-- How to read rules that could mean two things, e.g. "Last 5 games: all competitions". -->
