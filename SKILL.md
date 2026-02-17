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
4. Run:

python worklog.py --issue SUP-123 --hours 2.5 --comment "Refactored auth middleware"

## Notes

- Never modify estimates unless explicitly requested.
- Always confirm before logging time.
