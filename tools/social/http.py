"""Small HTTP layer. Real calls go through requests; tests swap in a fake with the same interface.
Errors never include query strings or headers (tokens live there)."""

import json


class HttpError(RuntimeError):
    def __init__(self, method, url, status, body):
        self.status = status
        super().__init__(f'{method} {url.split("?")[0]} → {status}: {body[:400]}')


class Response:
    def __init__(self, status, headers, body):
        self.status, self.headers, self.body = status, headers, body

    def json(self):
        try:
            return json.loads(self.body) if self.body else {}
        except ValueError:
            return {'raw': self.body}


class Http:
    def request(self, method, url, **kw):
        import requests
        kw.setdefault('timeout', 600)
        r = requests.request(method, url, **kw)
        resp = Response(r.status_code, dict(r.headers), r.text)
        if r.status_code >= 400:
            body = r.text
            for k in ('access_token', 'refresh_token', 'client_secret'):
                if k in body:
                    body = '<redacted>'
            raise HttpError(method, url, r.status_code, body)
        return resp

    def get(self, url, **kw):
        return self.request('GET', url, **kw).json()

    def post(self, url, **kw):
        return self.request('POST', url, **kw).json()
