"""Voiceover: edge-tts (en-AU male) first; Piper fallback when edge-tts can't reach Microsoft.

Fallback exists because some networks (e.g. cloud sandboxes) block the WebSocket edge-tts needs.
Set HOKO_PIPER_MODEL to a Piper .onnx voice to enable it. Returns the engine name used.

Proxy / CA (cloud runs): edge-tts verifies Microsoft's TLS against certifi's roots only, so behind a
TLS-re-terminating agent proxy the handshake fails with CERTIFICATE_VERIFY_FAILED. When SSL_CERT_FILE,
REQUESTS_CA_BUNDLE or the ccr bundle (/root/.ccr/ca-bundle.crt) is present, `edge_ssl_context()` builds a
*verifying* `ssl.create_default_context(cafile=<that bundle>)` and `_edge` hands it to edge-tts (both as the
aiohttp connector's context and as the context edge-tts pins on its WebSocket request — edge-tts 7.x passes
its own per-request context, which would otherwise override the connector). HTTPS_PROXY is passed through
as the WebSocket proxy because aiohttp's trust_env does not apply env proxies to wss:// URLs.
Certificate verification is never turned off. With none of those variables set (the PC) nothing changes:
no context is built, edge-tts runs exactly as before.
"""

import asyncio
import os
import ssl
import subprocess
import sys
from pathlib import Path

EDGE_VOICE = os.environ.get('HOKO_TTS_VOICE', 'en-AU-WilliamMultilingualNeural')
PIPER_VOICE = 'en_GB-alan-medium'                       # the fallback voice (same one the PC renders used)
PIPER_DEFAULT = Path(__file__).resolve().parent.parent / '.cache' / 'piper' / f'{PIPER_VOICE}.onnx'
CA_ENV_VARS = ('SSL_CERT_FILE', 'REQUESTS_CA_BUNDLE')   # standard CA-bundle variables, first one set wins
CCR_CA_BUNDLE = Path('/root/.ccr/ca-bundle.crt')        # Claude Code web agent-proxy bundle, used when it exists


def ca_bundle():
    """Path of the CA bundle to trust in addition to the defaults, or None (= PC, default context)."""
    for var in CA_ENV_VARS:
        v = os.environ.get(var)
        if v and Path(v).is_file():
            return Path(v)
    return CCR_CA_BUNDLE if CCR_CA_BUNDLE.is_file() else None


def edge_ssl_context():
    """A verifying SSL context built on the proxy CA bundle, or None when no bundle is configured.

    Never disables verification: `ssl.create_default_context` keeps CERT_REQUIRED + hostname checking,
    the cafile only adds the proxy CA to the trusted roots.
    """
    bundle = ca_bundle()
    if bundle is None:
        return None
    return ssl.create_default_context(cafile=str(bundle))


def edge_kwargs(ctx):
    """Extra Communicate() kwargs for a CA context: the connector carrying it + the env HTTPS proxy."""
    if ctx is None:
        return {}
    import aiohttp
    kw = {'connector': aiohttp.TCPConnector(ssl=ctx)}
    proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    if proxy:
        kw['proxy'] = proxy
    return kw


def piper_model():
    """HOKO_PIPER_MODEL if set, else the default download location (content/youtube/.cache/piper/)."""
    m = os.environ.get('HOKO_PIPER_MODEL')
    if m and Path(m).exists():
        return Path(m)
    return PIPER_DEFAULT if PIPER_DEFAULT.exists() else None


def _edge(text, out_mp3):
    import edge_tts
    ctx = edge_ssl_context()
    if ctx is not None:
        # edge-tts 7.x pins a module-level certifi context on every ws_connect (overrides the connector's);
        # point that at the same verifying context so the proxy CA is trusted there too.
        comm_mod = sys.modules.get('edge_tts.communicate')
        if comm_mod is not None and hasattr(comm_mod, '_SSL_CTX'):
            comm_mod._SSL_CTX = ctx

    async def go():
        kw = edge_kwargs(ctx)
        try:
            await edge_tts.Communicate(text, EDGE_VOICE, rate='+8%', **kw).save(str(out_mp3))
        finally:
            conn = kw.get('connector')
            if conn is not None and not conn.closed:
                await conn.close()
    asyncio.run(go())
    if not Path(out_mp3).exists() or Path(out_mp3).stat().st_size == 0:
        raise RuntimeError('edge-tts produced no audio')


def _piper(text, out_wav):
    model = piper_model()
    if not model:
        raise RuntimeError('HOKO_PIPER_MODEL not set / missing (cloud-run downloads en_GB-alan-medium to .cache/piper)')
    subprocess.run([sys.executable, '-m', 'piper', '-m', str(model), '-f', str(out_wav), '--length-scale', '0.92'],
                   input=text, text=True, check=True, capture_output=True)


def synth(text, out_base):
    """Write <out_base>.wav (always wav, 48k mono). Returns engine name."""
    out_base = Path(out_base)
    wav = out_base.with_suffix('.wav')
    tmp = out_base.with_suffix('.raw.audio')
    engine = None
    errors = []
    if os.environ.get('HOKO_TTS', '') != 'piper':
        try:
            _edge(text, tmp)
            engine = 'edge-tts:' + EDGE_VOICE
        except Exception as e:  # network / websocket blocked
            errors.append(f'edge-tts: {e.__class__.__name__}: {str(e)[:120]}')
    if engine is None:
        try:
            _piper(text, tmp)
            engine = 'piper:' + piper_model().stem
        except Exception as e:
            errors.append(f'piper: {e}')
            raise RuntimeError('No TTS engine worked — ' + ' | '.join(errors))
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(tmp), '-ac', '1', '-ar', '48000', str(wav)], check=True)
    tmp.unlink(missing_ok=True)
    return engine
