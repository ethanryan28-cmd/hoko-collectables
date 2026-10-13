"""Tiny HTTP layer so publish/comments can run against real APIs or canned (mocked) responses."""

import itertools
import json

import requests


class Http:
    mocked = False

    def get(self, url, **kw):
        r = requests.get(url, timeout=120, **kw)
        return _check(r)

    def post(self, url, **kw):
        r = requests.post(url, timeout=600, **kw)
        return _check(r)


def _check(r):
    try:
        j = r.json()
    except ValueError:
        j = {'raw': r.text}
    if r.status_code >= 400:
        raise RuntimeError(f'{r.request.method} {r.url.split("?")[0]} → {r.status_code}: {json.dumps(j)[:400]}')
    return j


class MockHttp(Http):
    """Returns responses shaped like the real Shopify / Instagram Graph APIs. Logs every call."""

    mocked = True

    def __init__(self):
        self.calls = []
        self._ids = itertools.count(17900000000000001)
        self._polls = 0

    def get(self, url, **kw):
        self.calls.append(('GET', url.split('?')[0]))
        if 'graph.facebook.com' in url:            # container status poll
            self._polls += 1
            return {'status_code': 'IN_PROGRESS' if self._polls < 2 else 'FINISHED', 'id': url.rsplit('/', 1)[-1]}
        return {}

    def post(self, url, **kw):
        self.calls.append(('POST', url.split('?')[0]))
        if url.endswith('/graphql.json'):
            q = (kw.get('json') or {}).get('query', '')
            if 'stagedUploadsCreate' in q:
                return {'data': {'stagedUploadsCreate': {'stagedTargets': [{
                    'url': 'https://shopify-video-production-core-originals.storage.googleapis.com/',
                    'resourceUrl': 'https://shopify-video-production-core-originals.storage.googleapis.com/?external_video_id=MOCK',
                    'parameters': [{'name': 'GoogleAccessId', 'value': 'mock'}]}], 'userErrors': []}}}
            if 'fileCreate' in q:
                return {'data': {'fileCreate': {'files': [{'id': 'gid://shopify/Video/MOCK1', 'fileStatus': 'UPLOADED'}],
                                                'userErrors': []}}}
            if 'node(' in q:
                return {'data': {'node': {'id': 'gid://shopify/Video/MOCK1', 'fileStatus': 'READY', 'sources': [
                    {'url': 'https://cdn.shopify.com/videos/c/vp/MOCK/MOCK.HD-1080p-7.2Mbps.mp4',
                     'mimeType': 'video/mp4', 'height': 1920, 'width': 1080}]}}}
        if 'storage.googleapis.com' in url:
            return {}
        if url.endswith('/media'):
            return {'id': str(next(self._ids))}
        if url.endswith('/media_publish'):
            return {'id': str(next(self._ids))}
        return {}
