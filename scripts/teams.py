"""Print the user's preferred teams, grouped by league.

The list comes from teams.xlsx in the skill's base directory (or a path given as an argument), or from
the teams table in Supabase when BETS_TEAMS_SOURCE=supabase, as in the daily agent's cloud runs.
`python scripts/teams.py --push` copies teams.xlsx into the Supabase table, replacing what's there.
Both have the columns League, Team, Role and Note. Roles:
  Pick                   a preferred team, backed against weaker teams on its league's terms
  Relegation games only  a preferred team, backed only against its league's relegation teams
  Relegation team        an opponent the user counts as a clear relegation team
Rows without a league, a team or a known role are skipped and listed at the end. A rules file can define
other roles: pass their names with --roles "Name|Other name".
"""
import os
import sys
from pathlib import Path

ROLES = ("Pick", "Relegation games only", "Relegation team")
COLUMNS = ("league", "team", "role", "note")
REPO = Path(__file__).resolve().parent.parent


def xlsx_rows(path):
    """(row number, league, team, role, note) for every non-empty row of the sheet."""
    from openpyxl import load_workbook

    if not path.exists():
        sys.exit(f"Team list not found: {path}")
    book = load_workbook(path, read_only=True, data_only=True)
    sheet = book["Teams"] if "Teams" in book.sheetnames else book.worksheets[0]
    rows = sheet.iter_rows(values_only=True)
    header = [str(cell or "").strip().lower() for cell in next(rows, ())]
    missing = [name for name in COLUMNS if name not in header]
    if missing:
        sys.exit(f"Team list is missing the column(s): {', '.join(missing)}")
    index = {name: header.index(name) for name in COLUMNS}
    for number, row in enumerate(rows, start=2):
        values = tuple(str(row[index[name]] or "").strip() if index[name] < len(row) else "" for name in COLUMNS)
        if any(values):
            yield (number, *values)


def supabase_rows():
    sys.path.insert(0, str(REPO))
    from agent.db import Db

    for number, row in enumerate(Db().select("teams", order="id"), start=1):
        yield (number, *(str(row.get(name) or "").strip() for name in COLUMNS))


def group(rows, names=ROLES):
    roles = {role.lower(): role for role in names}
    leagues, skipped = {}, []
    for number, league, team, role, note in rows:
        if not (league and team and role.lower() in roles):
            skipped.append(f"row {number}: {league or '?'} / {team or '?'} / {role or '?'}")
            continue
        leagues.setdefault(league, []).append((team, roles[role.lower()], note))
    return leagues, skipped


def push(path):
    sys.path.insert(0, str(REPO))
    from agent.db import Db

    leagues, skipped = group(xlsx_rows(path))
    if skipped:
        sys.exit("Fix these rows in teams.xlsx first:\n" + "\n".join(f"- {line}" for line in skipped))
    rows = [{"league": league, "team": team, "role": role, "note": note or None}
            for league, teams in leagues.items() for team, role, note in teams]
    db = Db()
    db.delete("teams", id="gt.0")
    db.insert("teams", rows)
    print(f"Copied {len(rows)} teams from {path.name} to Supabase.")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    argv, names = sys.argv[1:], ROLES
    if "--roles" in argv:
        at = argv.index("--roles")
        if at + 1 >= len(argv):
            sys.exit('--roles needs the role names, e.g. --roles "Pick|Fade"')
        names = tuple(name.strip() for name in argv[at + 1].split("|") if name.strip())
        argv = argv[:at] + argv[at + 2:]
    args = [a for a in argv if a != "--push"]
    path = Path(args[0]) if args else REPO / "teams.xlsx"
    if "--push" in argv:
        return push(path)
    source = os.environ.get("BETS_TEAMS_SOURCE", "xlsx").strip().lower()
    leagues, skipped = group(supabase_rows() if source == "supabase" and not args else xlsx_rows(path), names)

    if not leagues:
        sys.exit("Team list has no teams.")
    for league, teams in leagues.items():
        print(f"{league}:")
        for team, role, note in teams:
            print(f"- {team} ({role}{'; ' + note if note else ''})")
    if skipped:
        print(f"Skipped rows (each needs a league, a team and a role: {', '.join(names)}):")
        for line in skipped:
            print(f"- {line}")


if __name__ == "__main__":
    main()
