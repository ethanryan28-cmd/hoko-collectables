"""content/youtube/hoko/tts.py — proxy-CA handling for edge-tts.

Loaded by file path (content/youtube is a script tree, not a package). Nothing here needs edge-tts, aiohttp
or the network: edge_tts / aiohttp are stand-ins injected into sys.modules for the duration of each test.
"""

import importlib.util
import os
import ssl
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parents[3]
TTS_PATH = REPO / 'content' / 'youtube' / 'hoko' / 'tts.py'


def _load_tts():
    spec = importlib.util.spec_from_file_location('hoko_tts_under_test', TTS_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


NO_CA_ENV = {'SSL_CERT_FILE': '', 'REQUESTS_CA_BUNDLE': '', 'HTTPS_PROXY': '', 'https_proxy': ''}


class _FakeConnector:
    """Stands in for aiohttp.TCPConnector — records the ssl kwarg, no sockets."""
    instances = []

    def __init__(self, ssl=None):
        self.ssl = ssl
        self.closed = False
        _FakeConnector.instances.append(self)

    async def close(self):
        self.closed = True


class _FakeCommunicate:
    """Stands in for edge_tts.Communicate — records kwargs and writes a non-empty file on save()."""
    calls = []

    def __init__(self, text, voice, **kw):
        _FakeCommunicate.calls.append({'text': text, 'voice': voice, **kw})

    async def save(self, path):
        Path(path).write_bytes(b'ID3fake')


def _fake_modules(with_ssl_ctx=True):
    """edge_tts (+ edge_tts.communicate with/without _SSL_CTX) and aiohttp stand-ins."""
    comm = types.ModuleType('edge_tts.communicate')
    if with_ssl_ctx:
        comm._SSL_CTX = ssl.create_default_context()
    edge = types.ModuleType('edge_tts')
    edge.Communicate = _FakeCommunicate
    edge.communicate = comm
    aiohttp = types.ModuleType('aiohttp')
    aiohttp.TCPConnector = _FakeConnector
    return {'edge_tts': edge, 'edge_tts.communicate': comm, 'aiohttp': aiohttp}


class TTSProxyCA(unittest.TestCase):
    def setUp(self):
        _FakeConnector.instances.clear()
        _FakeCommunicate.calls.clear()
        self.tmp = tempfile.TemporaryDirectory()
        self.pem = Path(self.tmp.name) / 'proxy-ca.pem'
        # A real PEM bundle at a temp path (ssl really loads it): certifi's bundle when available, else the
        # interpreter's default verify file. Either way it is a copy, so the path is the temp one.
        try:
            import certifi
            src = Path(certifi.where())
        except ImportError:
            src = Path(ssl.get_default_verify_paths().cafile or '')
        if not src.is_file():
            self.skipTest('no PEM bundle available to copy')
        self.pem.write_bytes(src.read_bytes())

    def tearDown(self):
        self.tmp.cleanup()

    # --- edge_ssl_context ---------------------------------------------------------------------------

    def test_env_var_builds_context_with_that_cafile(self):
        tts = _load_tts()
        for var in ('SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE'):
            with self.subTest(var=var), mock.patch.dict(os.environ, {**NO_CA_ENV, var: str(self.pem)}), \
                    mock.patch.object(tts, 'CCR_CA_BUNDLE', Path(self.tmp.name) / 'absent.crt'), \
                    mock.patch.object(tts.ssl, 'create_default_context', wraps=ssl.create_default_context) as cdc:
                ctx = tts.edge_ssl_context()
                self.assertIsInstance(ctx, ssl.SSLContext)
                cdc.assert_called_once_with(cafile=str(self.pem))
                # verification stays ON
                self.assertEqual(ctx.verify_mode, ssl.CERT_REQUIRED)
                self.assertTrue(ctx.check_hostname)

    def test_ccr_bundle_used_when_no_env_var(self):
        tts = _load_tts()
        with mock.patch.dict(os.environ, NO_CA_ENV), mock.patch.object(tts, 'CCR_CA_BUNDLE', self.pem), \
                mock.patch.object(tts.ssl, 'create_default_context', wraps=ssl.create_default_context) as cdc:
            self.assertIsInstance(tts.edge_ssl_context(), ssl.SSLContext)
            cdc.assert_called_once_with(cafile=str(self.pem))

    def test_env_var_pointing_at_missing_file_is_ignored(self):
        tts = _load_tts()
        with mock.patch.dict(os.environ, {**NO_CA_ENV, 'SSL_CERT_FILE': str(self.pem) + '.nope'}), \
                mock.patch.object(tts, 'CCR_CA_BUNDLE', Path(self.tmp.name) / 'absent.crt'):
            self.assertIsNone(tts.edge_ssl_context())

    def test_no_env_var_means_no_context(self):
        """PC path: nothing set → None, and ssl.create_default_context is never touched."""
        tts = _load_tts()
        with mock.patch.dict(os.environ, NO_CA_ENV), \
                mock.patch.object(tts, 'CCR_CA_BUNDLE', Path(self.tmp.name) / 'absent.crt'), \
                mock.patch.object(tts.ssl, 'create_default_context') as cdc:
            self.assertIsNone(tts.edge_ssl_context())
            cdc.assert_not_called()
            self.assertEqual(tts.edge_kwargs(None), {})

    # --- _edge ---------------------------------------------------------------------------------------

    def test_edge_with_ca_passes_connector_proxy_and_pins_edge_tts_context(self):
        tts = _load_tts()
        fakes = _fake_modules(with_ssl_ctx=True)
        out = Path(self.tmp.name) / 'vo.raw.audio'
        with mock.patch.dict(sys.modules, fakes), \
                mock.patch.dict(os.environ, {**NO_CA_ENV, 'SSL_CERT_FILE': str(self.pem),
                                             'HTTPS_PROXY': 'http://127.0.0.1:3128'}), \
                mock.patch.object(tts, 'CCR_CA_BUNDLE', Path(self.tmp.name) / 'absent.crt'):
            tts._edge('g day', out)
        self.assertTrue(out.exists() and out.stat().st_size > 0)
        call = _FakeCommunicate.calls[-1]
        self.assertEqual(call['voice'], tts.EDGE_VOICE)
        self.assertEqual(call['proxy'], 'http://127.0.0.1:3128')
        conn = call['connector']
        self.assertIs(conn, _FakeConnector.instances[-1])
        self.assertIsInstance(conn.ssl, ssl.SSLContext)
        self.assertEqual(conn.ssl.verify_mode, ssl.CERT_REQUIRED)
        self.assertTrue(conn.ssl.check_hostname)
        # the context edge-tts pins on its WebSocket request is now the same verifying context
        self.assertIs(fakes['edge_tts.communicate']._SSL_CTX, conn.ssl)
        self.assertTrue(conn.closed)

    def test_edge_with_ca_but_no_proxy_env_omits_proxy(self):
        tts = _load_tts()
        fakes = _fake_modules(with_ssl_ctx=False)   # also covers an edge-tts without _SSL_CTX: no AttributeError
        out = Path(self.tmp.name) / 'vo.raw.audio'
        with mock.patch.dict(sys.modules, fakes), \
                mock.patch.dict(os.environ, {**NO_CA_ENV, 'REQUESTS_CA_BUNDLE': str(self.pem)}), \
                mock.patch.object(tts, 'CCR_CA_BUNDLE', Path(self.tmp.name) / 'absent.crt'):
            tts._edge('g day', out)
        call = _FakeCommunicate.calls[-1]
        self.assertNotIn('proxy', call)
        self.assertIn('connector', call)
        self.assertFalse(hasattr(fakes['edge_tts.communicate'], '_SSL_CTX'))

    def test_edge_without_ca_runs_default_path_unchanged(self):
        """PC behaviour: Communicate(text, voice, rate='+8%') only — no connector, no proxy, no context swap."""
        tts = _load_tts()
        fakes = _fake_modules(with_ssl_ctx=True)
        original_ctx = fakes['edge_tts.communicate']._SSL_CTX
        out = Path(self.tmp.name) / 'vo.raw.audio'
        with mock.patch.dict(sys.modules, fakes), mock.patch.dict(os.environ, NO_CA_ENV), \
                mock.patch.object(tts, 'CCR_CA_BUNDLE', Path(self.tmp.name) / 'absent.crt'):
            tts._edge('g day', out)
        call = _FakeCommunicate.calls[-1]
        self.assertEqual(set(call), {'text', 'voice', 'rate'})
        self.assertEqual(call['rate'], '+8%')
        self.assertIs(fakes['edge_tts.communicate']._SSL_CTX, original_ctx)
        self.assertEqual(_FakeConnector.instances, [])


if __name__ == '__main__':
    unittest.main()
