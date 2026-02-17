#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Missing environment variable: {name}")
    return value


def get_auth_header(email: str, token: str) -> str:
    raw = f"{email}:{token}".encode("utf-8")
    return "Basic " + base64.b64encode(raw).decode("ascii")


def ceil_to_quarter(dt: datetime) -> datetime:
    """Round a datetime UP to the next quarter hour."""
    minutes = dt.minute
    remainder = minutes % 15
    if remainder == 0 and dt.second == 0 and dt.microsecond == 0:
        return dt
    add = 15 - remainder
    return dt.replace(second=0, microsecond=0) + timedelta(minutes=add)


def compute_started(hours: float, start_time: Optional[str]) -> datetime:
    """Compute the worklog start datetime.

    If *start_time* is given (HH:MM), use today at that time.
    Otherwise, end = now rounded up to the next quarter hour, start = end − hours.
    """
    now = datetime.now(timezone.utc)
    if start_time:
        h, m = (int(x) for x in start_time.split(":"))
        return now.replace(hour=h, minute=m, second=0, microsecond=0)
    end = ceil_to_quarter(now)
    return end - timedelta(hours=hours)


def add_worklog(
    base_url: str,
    auth_header: str,
    issue_key: str,
    hours: float,
    comment: Optional[str],
    adjust_estimate: Optional[str] = None,
    start_time: Optional[str] = None,
):
    seconds = int(hours * 3600)
    started = compute_started(hours, start_time)

    payload = {
        "timeSpentSeconds": seconds,
        "started": started.strftime("%Y-%m-%dT%H:%M:%S.000+0000"),
    }

    if comment:
        payload["comment"] = {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": comment}],
                }
            ],
        }

    params = {}
    if adjust_estimate:
        params["adjustEstimate"] = adjust_estimate

    url = f"{base_url}/rest/api/3/issue/{issue_key}/worklog"

    r = requests.post(
        url,
        headers={
            "Authorization": auth_header,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        params=params,
        data=json.dumps(payload),
        timeout=30,
    )

    r.raise_for_status()
    return r.json()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", required=True)
    parser.add_argument("--hours", required=True, type=float)
    parser.add_argument("--comment", default="")
    parser.add_argument("--adjust", choices=["new", "leave", "manual"])
    parser.add_argument("--start", help="Start time as HH:MM (e.g. 08:00)")

    args = parser.parse_args()

    base_url = require_env("JIRA_BASE_URL").rstrip("/")
    email = require_env("JIRA_EMAIL")
    token = require_env("JIRA_API_TOKEN")

    auth = get_auth_header(email, token)

    result = add_worklog(
        base_url=base_url,
        auth_header=auth,
        issue_key=args.issue,
        hours=args.hours,
        comment=args.comment,
        adjust_estimate=args.adjust,
        start_time=args.start,
    )

    print("Worklog created successfully.")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
