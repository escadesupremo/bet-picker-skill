---
type: llm
focus: trace
weight: 1
---

The run worked from my-rules.md, not the skill's own rules.md: it didn't load the skill's team sheet (scripts/teams.py) and no row or description relies on a rule that's only in the skill's own rules.md (such as a form test, a European-game gap or a team list).
