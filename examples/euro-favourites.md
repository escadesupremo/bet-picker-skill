---
# My settings. Every rule with a number or a list lives here, and these are hard rules: a game that
# breaks one is dropped, even a marginal call. Everything below this block is in my words.

sports: [football, nfl]
draws: false                 # winner only, never a draw
odds_format: decimal         # decimal or american, for the table's Odds column
show_cost: true              # end each run with its tokens and their API cost

odds:
  min: 1.25
  max: 1.80
  hedge: rarely              # rarely outside this range
  by_league:                 # league games in these countries: a higher minimum, the same maximum
    France: {min: 1.30}
    Germany: {min: 1.30}
    Spain: {min: 1.30}
    Italy: {min: 1.30, hedge: more or less}
  nfl: {min: 1.30, max: 1.60, hedge: around}   # replaces the range above for the NFL

parlay:
  legs: [2, 3]
  total_odds: [1.80, 3.00]

form:
  last: 5                    # games
  competitions: all
  min_wins: 2
  max_losses: 2
  team: pick                 # only my pick's form can drop a game

european_gap:
  min_days: 4                # drop a league game if my team played in Europe fewer days before
  counts: before             # a European game after the league game doesn't count
  games: league              # league games, second divisions included
  exempt: [PSG, Bayern Munich, Barcelona, Real Madrid, Atlético Madrid, Man City, Arsenal]

roles:                       # what a team can be in the Team list
  Pick: a preferred team; back it against weaker teams on its league's terms
  Relegation games only: a preferred team; back it only against one of its league's Relegation teams
  Relegation team: an opponent I count as a clear relegation team; never a pick

---

# My betting rules

Big European favourites, the NFL against weak quarterbacks, and lopsided cup ties, in 2- or 3-game parlays.

## Ground rules
- European football and NFL only.
- Winner only, never a draw: the home or away win in football's regular-time 1X2 market, the moneyline in the NFL.
- In league games, the team I pick must be at least a better-known second-division club, such as a former top-flight side. A lesser-known second-division pick: rarely. A pick from below the second division: never. Cups have no such limit (see Cups). The opponent can come from any level.
- Only games where there's a reason to think my team is more likely to win that day than the odds suggest.

## Odds
- Rarely outside my range: below it the return is too small, above it the risk is too big.

## Parlays
- I combine the games into parlays myself, so list every game that passes.

## Form
- Check both teams' recent form in every football game.
- Few losses aren't enough on their own: W D D D L has only 1 loss, but just 1 win and 6 points out of 15, so it isn't good form.
- The opponent's form never drops a game. Give both teams' records in the description, e.g. "Last 5: Inter 4W 1D 0L, Venezia 1W 0D 4L."

## Team list
- The note is my own comment, such as "possibly" or "sometimes, as a fourth". Treat a hedge there like the other hedges.
- The list is my current view. Check positions against the current table, but don't add, drop or move teams: only I change the list.

| League | Team | Role | Note |
|---|---|---|---|
| England | Arsenal | Pick | top 2 |
| England | Man City | Pick | top 2 |
| England | Liverpool | Relegation games only | |
| England | Chelsea | Relegation games only | possibly |
| England | Coventry | Relegation team | |
| England | Ipswich | Relegation team | |
| France | PSG | Pick | |
| Germany | Bayern Munich | Pick | |
| Spain | Real Madrid | Pick | |
| Spain | Barcelona | Pick | |
| Spain | Atlético Madrid | Pick | |
| Italy | Inter | Pick | |
| Italy | Lazio | Pick | |
| Italy | Milan | Pick | |
| Portugal | Porto | Pick | |
| Portugal | Sporting | Pick | |
| Portugal | Benfica | Pick | |
| Portugal | Braga | Pick | sometimes, as a fourth |
| Scotland | Rangers | Pick | |
| Scotland | Celtic | Pick | |
| Croatia | Hajduk Split | Pick | |
| Austria | Red Bull Salzburg | Pick | |
| Hungary | Ferencváros | Pick | |
| Denmark | FC Copenhagen | Pick | |
| Denmark | Midtjylland | Pick | |
| Poland | Legia Warsaw | Pick | |
| Greece | AEK Athens | Pick | mostly AEK; not Olympiacos or Panathinaikos |
| Serbia | Red Star Belgrade | Pick | |
| Turkey | Fenerbahçe | Pick | |

## Leagues
I play every European first division. In the leagues that have teams in the list, back only the listed teams. The terms:
- **England:** a Pick team against a team at the lower end of the table, or any of England's listed teams against a Relegation team. Nothing else in England.
- **France and Germany:** against a team that isn't a clear contender that season.
- **Spain:** against a lower-table team.
- **Italy:** more or less the same terms as Spain.
- **Every other league in the list:** the team against a weaker one.
- **Second divisions** of the list's leagues: the same logic, though the list names no teams there. A historically great club that dominates the division, against a weaker team.
- **Every other European first division:** the historically great clubs that dominate there, against a weaker team. Only the first division: not its cups or second division.

## When I drop a league game
- The teams are close in the table, e.g. 2nd v 6th or 3rd v 8th.
- My team played a European game too few days before, e.g. Thursday then Sunday, Tuesday then Friday. Every team that isn't on the exempt list keeps this rule, listed teams included.

## Cups
- Every cup tie counts, at any level: a club from below the second division can be the pick, e.g. a League One side against a non-league side in the FA Cup. The team-level rule is for league games only.
- Games with a clear difference between the teams. The best case is odds in range and the teams in different divisions.
- Never when the teams are close, e.g. the lower-division team is near promotion and the higher-division team is near relegation.

## Marginal calls
When a game with one of the listed teams (Pick or Relegation games only) fails only on a judgement call that could go either way, include it anyway as a marginal call. Example: Porto (1st) v Académico de Viseu (6th) in the Taça da Liga, same division.
- Judgement calls: whether the teams are close in the table, whether there's a clear difference between them, whether the opponent is weak or low enough in the table.
- A clear fail isn't marginal: two title rivals (e.g. Man City 1st v Brighton 3rd), or a league game that matches my own drop examples (2nd v 6th, 3rd v 8th).

## Champions League, Europa League and Conference League
- Only very clear mismatches between the two countries' football.
- Almost any team against a team from Andorra, Liechtenstein or Gibraltar.
- Other very clear mismatches too, e.g. an English team against a North Macedonian or Albanian one.

## Internationals
- Any European national team's games: qualifiers, the Nations League, the Euros and friendlies.
- Clear skill differences only.
- The lowest tier (Liechtenstein, Andorra, Gibraltar) against any normally skilled team.
- Maybe the tier above too (Luxembourg, Lithuania, Latvia).

## NFL
- Almost always bet against a team whose starting QB is injured, or whose QB is low-skilled (bad record, e.g. Miami, Tennessee).
- Also games where form obviously favors one team.

## Where to look
- Leagues: fixtures involving the listed teams, the dominant clubs of the other European first divisions, and second-division games for a dominant big club.
- Cups: every domestic cup and league cup of the list's leagues that has games in the range, at every level, including early rounds between lower-division and non-league clubs (e.g. the FA Cup's first round).
- Cups, Europe and internationals: scan for the mismatches described above.

## Clarifications
How to read my rules where they could mean two things.
- The league drop rules apply to league games, second divisions included, but not to cups, Europe or internationals. The form rule applies to every football game.
- Cups: the domestic cups of the leagues in the list, league cups included (e.g. Portugal's Taça da Liga). Any team from any division can qualify, not just the listed ones, if the difference is clear.
- Team level: "better-known" is a judgement call. Count former top-flight clubs and big names; when it's borderline, say so in the description. The rule is about league games, so it doesn't apply to cups or internationals.
- Second divisions: the list names no teams there, so count a club only if it's historically big *and* clearly top of its division right now. Say why in its description.
- European first divisions: the top flights of UEFA's member countries. Where the list has no teams, count a club only if it has won that league many times *and* is still one of its top sides this season. Say why in its description. These clubs aren't listed teams, so they get no marginal calls.
