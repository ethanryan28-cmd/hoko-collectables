"""Shared bits for publishers. Every publisher module exposes:

  build(item, ctx)            -> payload dict (pure; no secrets — env values are inserted by send())
  validate(payload, item, ctx)-> list of problems (empty = valid)
  send(item, payload, http, ctx) -> remote id string

ctx keys: now (aware datetime), hosted_url (public clip URL or a placeholder), late (bool: slot already passed).
"""

from urllib.parse import urlparse

from .. import captions as cap

PLACEHOLDER_URL = 'https://cdn.shopify.com/videos/c/o/v/PLACEHOLDER.mp4'


def is_https(u):
    try:
        p = urlparse(u)
        return p.scheme == 'https' and bool(p.netloc)
    except ValueError:
        return False


def canon(*texts):
    out = []
    for t in texts:
        out += cap.check(t or '')
    return out


def need(payload, *keys):
    return [f'missing {k}' for k in keys if payload.get(k) in (None, '', [])]
