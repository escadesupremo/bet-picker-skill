"""Check a bet-picker rules file: its settings block, and its Team list table if it has one.

Usage: python scripts/check_rules.py [path]      (default: the rules file the skill would use)

Prints a one-line summary and exits 0 when the file is valid; otherwise lists every problem and exits 1.
Needs PyYAML (pip install pyyaml).
"""
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
SPORTS = {"football", "nfl"}
KEYS = {"sports", "draws", "odds_format", "show_cost", "odds", "parlay", "form", "european_gap", "roles",
        "teams", "rule_paths"}


def default_path():
    """The rules file the skill uses when the user names none: ~/.bet-picker/rules.md, else the skill's own."""
    home = Path.home() / ".bet-picker" / "rules.md"
    return home if home.exists() else SKILL / "rules.md"


def split(text):
    """(settings block, body) of a rules file, or raise ValueError."""
    lines = text.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("the file must start with a settings block between two --- lines")
    for end, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:end]), "\n".join(lines[end + 1:])
    raise ValueError("the settings block has no closing --- line")


def number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def check_range(name, value, problems, need_both=False):
    if not isinstance(value, dict):
        problems.append(f"{name} must be a map like {{min: 1.30, max: 1.80}}")
        return
    for key in value:
        if key not in ("min", "max", "hedge"):
            problems.append(f"{name}: unknown key '{key}' (use min, max, hedge)")
    for key in ("min", "max"):
        if key in value and not (number(value[key]) and value[key] > 1):
            problems.append(f"{name}.{key} must be decimal odds above 1, e.g. 1.30")
        elif need_both and key not in value:
            problems.append(f"{name}.{key} is missing")
    if number(value.get("min")) and number(value.get("max")) and value["min"] >= value["max"]:
        problems.append(f"{name}: min must be below max")


def check_settings(s, folder, problems):
    for key in s:
        if key not in KEYS:
            problems.append(f"unknown setting '{key}' (known: {', '.join(sorted(KEYS))})")
    sports = s.get("sports")
    if not (isinstance(sports, list) and sports and set(sports) <= SPORTS):
        problems.append("sports must be a list of football and/or nfl, e.g. [football, nfl]")
    for key in ("draws", "show_cost"):
        if key in s and not isinstance(s[key], bool):
            problems.append(f"{key} must be true or false")
    if s.get("odds_format", "decimal") not in ("decimal", "american"):
        problems.append("odds_format must be decimal or american")

    odds = s.get("odds")
    if odds is None:
        problems.append("odds is missing: the range for one pick, e.g. {min: 1.30, max: 1.80}")
    elif isinstance(odds, dict):
        by_league, nfl = odds.get("by_league"), odds.get("nfl")
        check_range("odds", {k: v for k, v in odds.items() if k not in ("by_league", "nfl")}, problems, True)
        if by_league is not None:
            if not isinstance(by_league, dict):
                problems.append("odds.by_league must map league names to ranges, e.g. Germany: {min: 1.30}")
            else:
                for league, bounds in by_league.items():
                    check_range(f"odds.by_league.{league}", bounds, problems)
        if nfl is not None:
            check_range("odds.nfl", nfl, problems)
    else:
        problems.append("odds must be a map like {min: 1.30, max: 1.80}")

    parlay = s.get("parlay")
    if parlay is not None:
        legs, total = (parlay.get("legs"), parlay.get("total_odds")) if isinstance(parlay, dict) else (None, None)
        if not (isinstance(legs, list) and legs and all(isinstance(n, int) and n >= 1 for n in legs)):
            problems.append("parlay.legs must list game counts, e.g. [2, 3], or [1] for singles")
        if total is not None and not (isinstance(total, list) and len(total) == 2 and all(map(number, total))
                                      and total[0] < total[1]):
            problems.append("parlay.total_odds must be [lowest, highest], e.g. [1.80, 3.00]")

    form = s.get("form")
    if form is not None:
        if not isinstance(form, dict):
            problems.append("form must be a map (last, competitions, min_wins, max_losses, team)")
        else:
            for key in ("last", "min_wins", "max_losses"):
                if key in form and not (isinstance(form[key], int) and form[key] >= 0):
                    problems.append(f"form.{key} must be a whole number")
            if not isinstance(form.get("last"), int) or form.get("last", 0) < 1:
                problems.append("form.last must be how many games, e.g. 5")
            if "min_wins" not in form and "max_losses" not in form:
                problems.append("form needs min_wins, max_losses or both")
            if form.get("competitions", "all") not in ("all", "league"):
                problems.append("form.competitions must be all or league")
            if form.get("team", "pick") != "pick":
                problems.append("form.team must be pick")
            form_sports = form.get("sports", ["football"])
            if not (isinstance(form_sports, list) and form_sports and set(form_sports) <= SPORTS):
                problems.append("form.sports must be a list of football and/or nfl")
            extra = set(form) - {"last", "competitions", "min_wins", "max_losses", "team", "sports"}
            if extra:
                problems.append(f"form: unknown key(s) {', '.join(sorted(extra))}")

    gap = s.get("european_gap")
    if gap is not None:
        if not isinstance(gap, dict):
            problems.append("european_gap must be a map (min_days, counts, games, exempt)")
        else:
            if not (isinstance(gap.get("min_days"), int) and gap["min_days"] >= 1):
                problems.append("european_gap.min_days must be a whole number of days, e.g. 4")
            if gap.get("counts", "before") not in ("before", "both"):
                problems.append("european_gap.counts must be before or both")
            if gap.get("games", "league") != "league":
                problems.append("european_gap.games must be league")
            exempt = gap.get("exempt", [])
            if not (isinstance(exempt, list) and all(isinstance(t, str) for t in exempt)):
                problems.append("european_gap.exempt must be a list of team names, e.g. [PSG, Arsenal]")
            known = {"champions league", "europa league", "conference league"}
            comps = gap.get("competitions", ["Champions League"])
            if not (isinstance(comps, list) and comps and all(isinstance(c, str) and c.strip().lower() in known
                                                              for c in comps)):
                problems.append("european_gap.competitions must list some of: Champions League, Europa League, "
                                "Conference League")
            extra = set(gap) - {"min_days", "counts", "games", "competitions", "exempt"}
            if extra:
                problems.append(f"european_gap: unknown key(s) {', '.join(sorted(extra))}")

    for key in ("roles", "rule_paths"):
        value = s.get(key)
        if value is not None and not (isinstance(value, dict) and value
                                      and all(isinstance(v, str) and v.strip() for v in value.values())):
            problems.append(f"{key} must map each name to what it means, e.g. Pick: a team I back")

    teams = s.get("teams")
    if teams is not None:
        if not isinstance(teams, str) or not teams.strip():
            problems.append("teams must be the path of a team sheet, e.g. teams.xlsx")
        elif not (folder / teams).exists():
            problems.append(f"teams: no sheet at {folder / teams}")


def team_table(body):
    """Rows (league, team, role, note) of the body's '## Team list' table, or None if it has none."""
    lines, inside, rows = body.splitlines(), False, None
    for line in lines:
        if line.startswith("## "):
            inside = line[3:].strip().lower() == "team list"
            continue
        if not inside or not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if rows is None:  # header
            rows = []
            continue
        if all(set(c) <= set("-: ") for c in cells):  # separator
            continue
        rows.append((cells + ["", "", "", ""])[:4])
    return rows


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    path = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else default_path()
    if not path.exists():
        sys.exit(f"No rules file at {path}.")
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML isn't installed: run  pip install pyyaml  and check again.")
    try:
        block, body = split(path.read_text(encoding="utf-8"))
        settings = yaml.safe_load(block) or {}
    except (ValueError, yaml.YAMLError) as error:
        sys.exit(f"{path}: the settings block doesn't parse: {error}")
    if not isinstance(settings, dict):
        sys.exit(f"{path}: the settings block must be a list of 'name: value' settings.")

    problems = []
    check_settings(settings, path.parent, problems)
    roles = settings.get("roles") or {}
    rows = team_table(body)
    if "teams" in settings:
        teams_note = f"teams in {settings['teams']}"
    elif rows is None:
        teams_note = "no team list"
    else:
        for number_, (league, team, role, _) in enumerate(rows, start=1):
            if not (league and team and role):
                problems.append(f"Team list row {number_}: needs a league, a team and a role")
            elif roles and role not in roles:
                problems.append(f"Team list row {number_} ({team}): role '{role}' isn't in the roles setting")
        if rows and not roles:
            problems.append("the Team list has rows but the settings have no roles")
        teams_note = f"{len(rows)} team{'s' if len(rows) != 1 else ''} in the Team list"
    if not any(line.startswith("## ") for line in body.splitlines()):
        problems.append("the rules below the settings have no ## headings")

    if problems:
        print(f"{path} has {len(problems)} problem{'s' if len(problems) != 1 else ''}:")
        for problem in problems:
            print(f"- {problem}")
        sys.exit(1)
    odds = settings["odds"]
    print(f"{path} is valid: {' and '.join(s.upper() if s == 'nfl' else s for s in settings['sports'])}, "
          f"odds {odds['min']:.2f}–{odds['max']:.2f}, {teams_note}.")


if __name__ == "__main__":
    main()
