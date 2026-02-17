# jira-worklog

A [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code/skills) that logs time (worklogs) to Jira issues via the Jira REST API v3.

## Setup

### Prerequisites

- Python 3
- `requests` library (`pip install requests`)

### Environment Variables

Set the following environment variables:

| Variable | Description |
|---|---|
| `JIRA_BASE_URL` | Your Jira instance URL (e.g. `https://yourcompany.atlassian.net`) |
| `JIRA_EMAIL` | Email address associated with your Jira account |
| `JIRA_API_TOKEN` | Jira API token ([generate one here](https://id.atlassian.com/manage-profile/security/api-tokens)) |

## Usage

### As a Claude Code Skill

When installed as a skill, Claude will automatically use this when you mention logging time to a Jira issue. For example:

> "I spent 2 hours on SUP-123 refactoring auth middleware"

Claude will confirm the details before logging.

### Standalone

```bash
python worklog.py --issue SUP-123 --hours 2.5 --comment "Refactored auth middleware"
```

#### Arguments

| Argument | Required | Description |
|---|---|---|
| `--issue` | Yes | Jira issue key (e.g. `SUP-123`) |
| `--hours` | Yes | Time spent in hours (supports decimals) |
| `--comment` | No | Work description |
| `--adjust` | No | Estimate adjustment strategy: `new`, `leave`, or `manual` |
