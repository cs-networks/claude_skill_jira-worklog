from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest

from worklog import ceil_to_quarter, compute_started


class TestCeilToQuarter:
    def test_exact_quarter_unchanged(self):
        dt = datetime(2026, 2, 17, 8, 0, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == dt

    def test_exact_quarter_15(self):
        dt = datetime(2026, 2, 17, 8, 15, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == dt

    def test_exact_quarter_30(self):
        dt = datetime(2026, 2, 17, 8, 30, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == dt

    def test_exact_quarter_45(self):
        dt = datetime(2026, 2, 17, 8, 45, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == dt

    def test_one_minute_past_rounds_up(self):
        dt = datetime(2026, 2, 17, 8, 1, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == datetime(2026, 2, 17, 8, 15, 0, 0, tzinfo=timezone.utc)

    def test_14_minutes_rounds_up(self):
        dt = datetime(2026, 2, 17, 8, 14, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == datetime(2026, 2, 17, 8, 15, 0, 0, tzinfo=timezone.utc)

    def test_16_minutes_rounds_up(self):
        dt = datetime(2026, 2, 17, 8, 16, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == datetime(2026, 2, 17, 8, 30, 0, 0, tzinfo=timezone.utc)

    def test_44_minutes_rounds_up(self):
        dt = datetime(2026, 2, 17, 8, 44, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == datetime(2026, 2, 17, 8, 45, 0, 0, tzinfo=timezone.utc)

    def test_46_minutes_rounds_to_next_hour(self):
        dt = datetime(2026, 2, 17, 8, 46, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == datetime(2026, 2, 17, 9, 0, 0, 0, tzinfo=timezone.utc)

    def test_seconds_cause_rounding(self):
        dt = datetime(2026, 2, 17, 8, 0, 1, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == datetime(2026, 2, 17, 8, 15, 0, 0, tzinfo=timezone.utc)

    def test_microseconds_cause_rounding(self):
        dt = datetime(2026, 2, 17, 8, 0, 0, 1, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == datetime(2026, 2, 17, 8, 15, 0, 0, tzinfo=timezone.utc)

    def test_59_minutes_rounds_to_next_hour(self):
        dt = datetime(2026, 2, 17, 23, 59, 0, 0, tzinfo=timezone.utc)
        assert ceil_to_quarter(dt) == datetime(2026, 2, 18, 0, 0, 0, 0, tzinfo=timezone.utc)


class TestComputeStarted:
    @patch("worklog.datetime")
    def test_explicit_start_time(self, mock_dt):
        now = datetime(2026, 2, 17, 14, 22, 33, 0, tzinfo=timezone.utc)
        mock_dt.now.return_value = now
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        result = compute_started(8.0, "08:00")
        assert result == datetime(2026, 2, 17, 8, 0, 0, 0, tzinfo=timezone.utc)

    @patch("worklog.datetime")
    def test_explicit_start_time_non_zero_minutes(self, mock_dt):
        now = datetime(2026, 2, 17, 14, 22, 33, 0, tzinfo=timezone.utc)
        mock_dt.now.return_value = now
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        result = compute_started(2.0, "10:30")
        assert result == datetime(2026, 2, 17, 10, 30, 0, 0, tzinfo=timezone.utc)

    @patch("worklog.datetime")
    def test_no_start_time_auto_computes(self, mock_dt):
        # now = 14:22 → ceil = 14:30 → start = 14:30 - 2h = 12:30
        now = datetime(2026, 2, 17, 14, 22, 0, 0, tzinfo=timezone.utc)
        mock_dt.now.return_value = now
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        result = compute_started(2.0, None)
        assert result == datetime(2026, 2, 17, 12, 30, 0, 0, tzinfo=timezone.utc)

    @patch("worklog.datetime")
    def test_no_start_time_exact_quarter(self, mock_dt):
        # now = 14:00 exactly → ceil = 14:00 → start = 14:00 - 1h = 13:00
        now = datetime(2026, 2, 17, 14, 0, 0, 0, tzinfo=timezone.utc)
        mock_dt.now.return_value = now
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        result = compute_started(1.0, None)
        assert result == datetime(2026, 2, 17, 13, 0, 0, 0, tzinfo=timezone.utc)

    @patch("worklog.datetime")
    def test_no_start_time_fractional_hours(self, mock_dt):
        # now = 10:07 → ceil = 10:15 → start = 10:15 - 2.5h = 07:45
        now = datetime(2026, 2, 17, 10, 7, 0, 0, tzinfo=timezone.utc)
        mock_dt.now.return_value = now
        mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)

        result = compute_started(2.5, None)
        assert result == datetime(2026, 2, 17, 7, 45, 0, 0, tzinfo=timezone.utc)
