"""Env-only config for the social auto-poster. Values are never printed; only key names and set/missing."""

import os
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CONTENT = REPO / 'content'
YT_CONTENT = CONTENT / 'youtube'
DATA = REPO / 'data'
QUEUE_PATH = CONTENT / 'social-queue.json'
LOG_PATH = DATA / 'social-post-log.csv'
MEDIA_CACHE_PATH = DATA / 'social-media-cache.json'
DRYRUN_PATH = DATA / 'social-dryrun.json'
RUNNER_LOG_PATH = DATA / 'social-runner.log'     # cloud-run transcript (committed with the CSV)

TZ_NAME = 'Australia/Melbourne'
SITE = 'https://www.hokocollectables.com'
GRAPH = 'https://graph.facebook.com/v21.0'
GRAPH_VIDEO = 'https://graph-video.facebook.com/v21.0'
SHOPIFY_API = '2025-01'

# key -> (platform, what it is). Order = order printed by `env`.
KEYS = {
    'META_PAGE_TOKEN': ('instagram+facebook', 'long-lived Facebook Page access token (also used for the IG Graph API)'),
    'IG_BUSINESS_ID': ('instagram', 'Instagram professional account id linked to the Page'),
    'FB_PAGE_ID': ('facebook', 'Facebook Page id'),
    'YT_CLIENT_ID': ('youtube', 'Google OAuth client id'),
    'YT_CLIENT_SECRET': ('youtube', 'Google OAuth client secret'),
    'YT_REFRESH_TOKEN': ('youtube', 'OAuth refresh token with youtube.upload scope'),
    'PINTEREST_TOKEN': ('pinterest', 'Pinterest v5 access token with pins:write, boards:read'),
    'PINTEREST_BOARD_ID': ('pinterest', 'board the pins go to'),
    'DISCORD_WEBHOOK_URL': ('discord', 'webhook URL for #pickups-and-drops'),
    'DISCORD_WEBHOOK_PICKUPS': ('discord', 'old name for DISCORD_WEBHOOK_URL, still read if that is unset'),
    'DISCORD_WEBHOOK_TIKTOK_QUEUE': ('tiktok', 'webhook URL for #tiktok-queue (clips + captions for the phone)'),
    'TIKTOK_ENABLED': ('tiktok', 'true to post via the Content Posting API (default false)'),
    'TIKTOK_CLIENT_KEY': ('tiktok', 'TikTok app client key (only if TIKTOK_ENABLED=true)'),
    'TIKTOK_CLIENT_SECRET': ('tiktok', 'TikTok app client secret (only if TIKTOK_ENABLED=true)'),
    'TIKTOK_REFRESH_TOKEN': ('tiktok', 'TikTok user refresh token, video.publish scope (only if TIKTOK_ENABLED=true)'),
    'SHOPIFY_STORE': ('instagram+facebook', 'xxxx.myshopify.com, for hosting reels on Shopify Files'),
    'SHOPIFY_ADMIN_TOKEN': ('instagram+facebook', 'Admin API token with write_files'),
}

# which keys each platform needs to post for real
NEEDS = {
    'instagram': ['META_PAGE_TOKEN', 'IG_BUSINESS_ID', 'SHOPIFY_STORE', 'SHOPIFY_ADMIN_TOKEN'],
    'facebook': ['META_PAGE_TOKEN', 'FB_PAGE_ID', 'SHOPIFY_STORE', 'SHOPIFY_ADMIN_TOKEN'],
    'youtube': ['YT_CLIENT_ID', 'YT_CLIENT_SECRET', 'YT_REFRESH_TOKEN'],
    'pinterest': ['PINTEREST_TOKEN', 'PINTEREST_BOARD_ID'],
    'discord': ['DISCORD_WEBHOOK_URL'],
    'tiktok_queue': ['DISCORD_WEBHOOK_TIKTOK_QUEUE'],
    'tiktok': ['TIKTOK_CLIENT_KEY', 'TIKTOK_CLIENT_SECRET', 'TIKTOK_REFRESH_TOKEN', 'SHOPIFY_STORE', 'SHOPIFY_ADMIN_TOKEN'],
    'shopify_files': ['SHOPIFY_STORE', 'SHOPIFY_ADMIN_TOKEN'],     # hosting clips for IG / FB / TikTok
}
# order used by `env` and cloud-run. tiktok = direct API (needs TIKTOK_ENABLED=true); tiktok_queue = phone pack via Discord
PLATFORM_ORDER = ['instagram', 'facebook', 'youtube', 'pinterest', 'discord', 'tiktok_queue', 'tiktok', 'shopify_files']


# new key name -> older names still read when the new one is unset
ALIASES = {'DISCORD_WEBHOOK_URL': ('DISCORD_WEBHOOK_PICKUPS',)}


def get(key, default=None):
    for k in (key, *ALIASES.get(key, ())):
        v = os.environ.get(k)
        if v not in (None, ''):
            return v
    return default


def tiktok_enabled():
    return (get('TIKTOK_ENABLED', 'false') or '').strip().lower() in ('1', 'true', 'yes')


def missing(platform):
    """Env keys this platform still needs. For the TikTok API, TIKTOK_ENABLED=true counts as a key."""
    out = [k for k in NEEDS[platform] if not get(k)]
    if platform == 'tiktok' and not tiktok_enabled():
        out.insert(0, 'TIKTOK_ENABLED')
    return out


def platform_lines():
    """One line per platform: '<platform>: set' or '<platform>: MISSING A, B'. Never a value."""
    out = []
    for p in PLATFORM_ORDER:
        m = missing(p)
        out.append(f'{p}: set' if not m else f'{p}: MISSING {", ".join(m)}')
    return out


def env_report():
    """Lines like 'META_PAGE_TOKEN   set      instagram+facebook  …' — never the value."""
    out = []
    w = max(len(k) for k in KEYS)
    for k, (plat, what) in KEYS.items():
        out.append(f'{k:<{w}}  {"set" if get(k) else "MISSING":<7}  {plat:<18}  {what}')
    return out


# --- newest-set ("hot") push — read from content/youtube/config.json -----------------------------------------
HOT_CONFIG_PATH = YT_CONTENT / 'config.json'
HOT_SHARE_DEFAULT = 0.6          # share of queue slots the hot sets must take (gate in `check`)
HOT_REPEAT_DAYS_DEFAULT = 2      # a hot asset may repeat on the same platform after this many days (others: 7)
BF_WEEK = ('2026-11-20', '2026-11-30')   # Black Friday week block: every caption carries the BF line


def hot_config():
    """hot_sets, hot share and hot repeat window from content/youtube/config.json (never throws)."""
    import json
    try:
        cfg = json.loads(HOT_CONFIG_PATH.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        cfg = {}
    return {'hot_sets': list(cfg.get('hot_sets') or []),
            'share': float(cfg.get('social_hot_share', HOT_SHARE_DEFAULT)),
            'repeat_days': int(cfg.get('social_hot_repeat_days', HOT_REPEAT_DAYS_DEFAULT))}
