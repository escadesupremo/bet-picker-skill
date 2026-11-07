# Sources

Where to find what the workflow needs, from earlier runs. Sites change and block automated fetches without warning, so when one fails, search for another; don't fall back on memory.

**Check the season on every figure.** Search results and their summaries often mix in last season's pages: a table, a result or a fixture can be a year old. Use a figure only when its page shows the current season and date.

## Odds and fixtures
- **OddsPortal** lists upcoming fixtures with average 1X2 or moneyline odds, one page per competition: `https://www.oddsportal.com/football/<country>/<competition>/`.
  - Worked: `england/premier-league`, `england/championship`, `england/league-cup`, `spain/laliga`, `spain/laliga2`, `spain/copa-del-rey`, `italy/serie-a`, `italy/serie-b`, `germany/bundesliga`, `germany/2-bundesliga`, `germany/dfb-pokal`, `france/ligue-1`, `france/ligue-2`, `portugal/league-cup`, `scotland/premiership`, `scotland/championship`, `croatia/hnl`, `austria/bundesliga`, `austria/ofb-cup`.
  - NFL: `https://www.oddsportal.com/american-football/usa/nfl/`.
  - For other competitions, guess the slug the same way, or search "oddsportal <competition>".
  - It shows each game's average and best price. Say which one a table uses when they differ much.
- **betexplorer.com** has a fixtures page per league with the bookmakers' average 1X2, e.g. `https://www.betexplorer.com/football/germany/bundesliga/fixtures/`. It worked for the smaller top flights too, and its team pages list results in all competitions.
- **Cup prices** are often missing from comparison sites in early rounds. Search for a betting preview of the game instead ("<home> vs <away> tip odds"): tipster sites such as wettbasis.com (DFB-Pokal) and bookmakers' own previews quote prices. Search rather than guess their URLs, which often 404.
- **footballwebpages.co.uk** lists every game of a day (`https://www.footballwebpages.co.uk/YYYYMMDD`) and each English competition's fixtures, tables and form, down to non-league. Automated page fetches get 403; downloading the page with curl worked.
- **Blocked:** Oddschecker and fbref.com return 403.

## Tables
- **ESPN standings:** `https://www.espn.com/soccer/standings/_/league/<code>`.
  - Worked: `eng.1`, `esp.1`, `esp.2`, `ita.1`, `ger.1`, `ger.2`, `fra.1`, `por.1`, `sco.1`, `aut.1`.
  - Second divisions usually follow the pattern (`eng.2`, `ita.2`, `fra.2`).
- **Transfermarkt** has each league's table and each club's season schedule with results, e.g. `https://www.transfermarkt.com/fc-bayern-munchen/spielplan/verein/27/saison_id/<season start year>`.
- **Blocked:** BBC Sport.

## Results and form
- **ESPN scoreboards** list one day's games, home team first, with scores: `https://www.espn.com/soccer/scoreboard/_/league/<code>/date/YYYYMMDD`. They're the most reliable way to check a result. European codes: `uefa.champions`, `uefa.europa`, `uefa.europa.conf`.
- **ESPN team results** (`https://www.espn.com/soccer/team/results/_/id/<id>`) list a team's games in all competitions, but don't always make clear which score is whose. Check doubtful results on the scoreboard for that day.
- **FotMob** team pages (`https://www.fotmob.com/teams/<id>/overview/<name>`) work for clubs ESPN covers badly, e.g. lower divisions. Some language versions show old data.
- **The LiveScore MCP server** (livescoremcp.com, in `.mcp.json`) has fixtures, tables and results for 1,000+ leagues, including the smaller European ones, when it's enabled.
- Searching "<team> results <month> <year>" also works for single teams.

## European fixtures
- uefa.com publishes each competition's full fixture list. Use it to check whether a team played in Europe within a few days of a league game. The Champions League usually plays Tuesday and Wednesday, the Europa League and Conference League Thursday.

## NFL
- **Injuries:** `https://www.espn.com/nfl/injuries`.
- **Standings and records:** `https://www.espn.com/nfl/standings`.
- **Starting QBs:** SI keeps a weekly list (search "every starting NFL quarterback <season>"). Check a doubtful QB with a search for that game's preview.
