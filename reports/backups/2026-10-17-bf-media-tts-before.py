"""Voiceover: edge-tts (en-AU male) first; Piper fallback when edge-tts can't reach Microsoft.

Fallback exists because some networks (e.g. cloud sandboxes) block the WebSocket edge-tts needs.
Set HOKO_PIPER_MODEL to a Piper .onnx voice to enable it. Returns the engine name used.
"""

import asyncio
import os
import subprocess
import sys
from pathlib import Path

EDGE_VOICE = os.environ.get('HOKO_TTS_VOICE', 'en-AU-WilliamMultilingualNeural')
PIPER_VOICE = 'en_GB-alan-medium'                       # the fallback voice (same one the PC renders used)
PIPER_DEFAULT = Path(__file__).resolve().parent.parent / '.cache' / 'piper' / f'{PIPER_VOICE}.onnx'


def piper_model():
    """HOKO_PIPER_MODEL if set, else the default download location (content/youtube/.cache/piper/)."""
    m = os.environ.get('HOKO_PIPER_MODEL')
    if m and Path(m).exists():
        return Path(m)
    return PIPER_DEFAULT if PIPER_DEFAULT.exists() else None


def _edge(text, out_mp3):
    import edge_tts

    async def go():
        await edge_tts.Communicate(text, EDGE_VOICE, rate='+8%').save(str(out_mp3))
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
