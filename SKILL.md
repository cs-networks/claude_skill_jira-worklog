---
name: jira-worklog
description: Log time (worklogs) to Jira issues. Use when the user says they worked on a Jira ticket, spent time on an issue, or want to log hours.
---

# Jira Worklog Skill

This skill logs time to Jira issues.

## Required environment variables

JIRA_BASE_URL
JIRA_EMAIL
JIRA_API_TOKEN

## Workflow

1. Extract issue key (e.g. SUP-123)
2. Extract time (explicit or natural language)
3. Confirm action
4. Run the appropriate command (see examples below)

## Start-time logic

- **Full day / no start time mentioned**: use `--start 08:00 --hours 8`
- **Specific duration, no explicit start**: omit `--start` — the script auto-computes start = (current time rounded up to next quarter hour) − duration
- **Explicit start time given by user**: pass `--start HH:MM`

## Examples

```bash
# "I worked on SUP-123 the whole day"
python worklog.py --issue SUP-123 --hours 8 --start 08:00 --comment "Feature work"

# "I spent 2.5 hours on SUP-123" (auto-computes start from now)
python worklog.py --issue SUP-123 --hours 2.5 --comment "Refactored auth middleware"

# "I worked on SUP-123 from 10:00 for 3 hours"
python worklog.py --issue SUP-123 --hours 3 --start 10:00 --comment "Code review"
```

## Notes

- Never modify estimates unless explicitly requested.
- Always confirm before logging time.
