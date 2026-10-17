"""Posting slots (Australia/Melbourne) and time helpers."""

from datetime import date, datetime, time, timedelta

try:
    from zoneinfo import ZoneInfo
    TZ = ZoneInfo('Australia/Melbourne')
except Exception as e:  # Windows without tzdata
    raise SystemExit('zoneinfo has no Australia/Melbourne — run: pip install tzdata') from e

SLOTS = {
    'youtube': ['11:00', '18:00'],
    'instagram': ['12:15', '19:15'],
    'facebook': ['12:15', '19:15'],     # mirrors Instagram
    'pinterest': ['10:00', '15:00', '20:00'],
    'discord': ['17:00'],               # → #pickups-and-drops
    'tiktok_queue': ['07:00'],          # one package of TIKTOK_PER_DAY clips → #tiktok-queue
}
TIKTOK_PER_DAY = 3
PLATFORMS = list(SLOTS)
VIDEO_PLATFORMS = ('youtube', 'instagram', 'facebook', 'tiktok_queue')

# how long after its slot an item may still go out before it is logged SKIP (stale)
LATE_GRACE = timedelta(hours=6)
YT_HORIZON = timedelta(days=14)        # upload every YT item due in the next 14 days (publishAt)
FB_MIN_LEAD = timedelta(minutes=15)    # Facebook wants scheduled_publish_time >= 10 min ahead
FB_HORIZON = timedelta(days=14)


def now():
    return datetime.now(TZ)


def slot_dt(day, hhmm):
    h, m = map(int, hhmm.split(':'))
    return datetime.combine(day, time(h, m), tzinfo=TZ)


def parse(s):
    d = datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=TZ)


def days(start, n):
    return [start + timedelta(days=i) for i in range(n)]


def local_date(dt):
    return dt.astimezone(TZ).date()


def season_weights(day: date):
    """Target category shares. Japanese sealed weighted heavier through November."""
    if day.month in (10, 11):
        return {'jp': 0.70, 'slab': 0.20, 'other': 0.10}
    return {'jp': 0.50, 'slab': 0.30, 'other': 0.20}
