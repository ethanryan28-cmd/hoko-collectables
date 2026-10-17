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
    'DISCORD_WEBHOOK_PICKUPS': ('discord', 'webhook URL for #pickups-and-drops'),
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
    'discord': ['DISCORD_WEBHOOK_PICKUPS'],
    'tiktok_queue': ['DISCORD_WEBHOOK_TIKTOK_QUEUE'],
    'tiktok': ['TIKTOK_CLIENT_KEY', 'TIKTOK_CLIENT_SECRET', 'TIKTOK_REFRESH_TOKEN', 'SHOPIFY_STORE', 'SHOPIFY_ADMIN_TOKEN'],
}


def get(key, default=None):
    v = os.environ.get(key)
    return v if v not in (None, '') else default


def tiktok_enabled():
    return (get('TIKTOK_ENABLED', 'false') or '').strip().lower() in ('1', 'true', 'yes')


def missing(platform):
    return [k for k in NEEDS[platform] if not get(k)]


def env_report():
    """Lines like 'META_PAGE_TOKEN   set      instagram+facebook  …' — never the value."""
    out = []
    w = max(len(k) for k in KEYS)
    for k, (plat, what) in KEYS.items():
        out.append(f'{k:<{w}}  {"set" if get(k) else "MISSING":<7}  {plat:<18}  {what}')
    return out
