"""Shorts from long-form + packaging.

run.py shorts           inbox/*.mp4 → transcript → 3–5 clips (20–55s, strongest hooks) → vertical crop,
                        burned captions, end card → out/<video>/short_N.mp4 + short_N.json
run.py package <video>  3 title variants + 3 thumbnails 1280x720 → out/<video>/package/
"""

import json
import os
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw

from .common import FONT_BLACK, ROOT, H, W, ffprobe
from .reel import end_card, font, wrap  # shared with reels

INBOX = ROOT / 'inbox'
OUT = ROOT / 'out'
MIN_S, MAX_S = 20.0, 55.0
TAGS = ['#Shorts', '#pokemontcg', '#onepiecetcg', '#tcg', '#sealedproduct', '#gradedcards', '#tcgaustralia',
        '#aussiecollector', '#hokocollectables']

HOOK_WORDS = re.compile(r'\b(never|nobody|biggest|best|worst|insane|crazy|worth|psa ?10|gem|pulled|pull|chase|'
                        r'secret|mistake|don\'t|stop|why|how|what|this is|you|your|\$\d+|\d+ dollars?)\b', re.I)


# ---------------------------------------------------------------- transcript

def transcribe(video, model='small'):
    """faster-whisper segments with word timings, cached next to outputs."""
    cache = OUT / video.stem / 'transcript.json'
    if cache.exists():
        return json.loads(cache.read_text())
    from faster_whisper import WhisperModel
    import numpy as np
    m = WhisperModel(model, device='auto', compute_type='int8')
    # decode with ffmpeg ourselves: faster-whisper's PyAV path breaks across av versions
    pcm = subprocess.run(['ffmpeg', '-v', 'error', '-i', str(video), '-vn', '-ac', '1', '-ar', '16000', '-f', 's16le', '-'],
                         capture_output=True, check=True).stdout
    audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0
    if audio.size == 0:
        return []
    segs, info = m.transcribe(audio, word_timestamps=True, vad_filter=True)
    out = [{'start': s.start, 'end': s.end, 'text': s.text.strip(),
            'words': [{'start': w.start, 'end': w.end, 'word': w.word} for w in (s.words or [])]} for s in segs]
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(out, indent=1))
    return out


def sentences(segs):
    """Re-split whisper segments into sentences using word timings (whisper cuts mid-sentence)."""
    words = [w for s in segs for w in s.get('words', [])]
    if not words:
        return segs
    out, cur = [], []
    for w in words:
        cur.append(w)
        if w['word'].strip().endswith(('.', '!', '?')):
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return [{'start': c[0]['start'], 'end': c[-1]['end'], 'text': ''.join(x['word'] for x in c).strip(), 'words': c}
            for c in out]


def hook_score(text):
    first = re.split(r'(?<=[.!?])\s', text.strip())[0]
    s = len(HOOK_WORDS.findall(first)) * 2.0
    s += 2.0 if first.endswith('?') else 0
    s += 1.5 if re.search(r'\d', first) else 0
    s -= 0.05 * max(0, len(first.split()) - 14)      # long-winded openers are weak hooks
    return s


def pick_clips(segs, duration, n_max=5):
    segs = sentences(segs)
    cands = []
    for i, s in enumerate(segs):
        end, j, words = s['end'], i, 0
        while j < len(segs) and segs[j]['end'] - s['start'] <= MAX_S:
            end = segs[j]['end']
            words += len(segs[j]['text'].split())
            if end - s['start'] >= MIN_S and segs[j]['text'].rstrip().endswith(('.', '!', '?')):
                dens = words / (end - s['start'])
                cands.append((hook_score(s['text']) + min(dens, 3.5), s['start'], end, s['text']))
            j += 1
    if not cands:                                    # no speech (or no sentence ends) → fixed windows
        step = max(MIN_S, min(40.0, duration / 3))
        t, k = 0.0, 0
        while t + MIN_S <= duration and k < 3:
            cands.append((0, t, min(t + step, duration), ''))
            t += step
            k += 1
        if not cands and duration > 3:
            cands.append((0, 0.0, min(duration, MAX_S), ''))
    cands.sort(key=lambda c: -c[0])
    chosen = []
    for c in cands:
        if all(c[2] <= o[1] or c[1] >= o[2] for o in chosen):
            chosen.append(c)
        if len(chosen) == n_max:
            break
    return sorted(chosen, key=lambda c: c[1])


# ---------------------------------------------------------------- captions (ASS)

def ass_time(t):
    t = max(0.0, t)
    return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'


def write_ass(segs, start, end, path):
    words = [w for s in segs for w in s['words'] if w['start'] >= start - 0.05 and w['end'] <= end + 0.05]
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display Black,112,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,1,0,0,0,100,100,0,0,1,9,2,2,70,70,520,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    for i in range(0, len(words), 3):
        chunk = words[i:i + 3]
        txt = ' '.join(w['word'].strip() for w in chunk).upper().replace('{', '').replace('}', '')
        a, b = chunk[0]['start'] - start, chunk[-1]['end'] - start
        if i + 3 < len(words):
            b = max(b, words[i + 3]['start'] - start)
        lines.append(f'Dialogue: 0,{ass_time(a)},{ass_time(b)},Cap,,0,0,0,,{txt}')
    path.write_text(head + '\n'.join(lines) + '\n', encoding='utf-8')
    return len(lines)


# ---------------------------------------------------------------- render

def cut_short(video, start, end, ass, out_mp4, endcard_png):
    """Vertical centre-crop + burned captions + 2s end card. ffmpeg runs inside the output dir so the
    subtitles filter gets plain relative paths (Windows drive-letter colons break filter args)."""
    cwd = out_mp4.parent
    fonts = os.path.relpath(FONT_BLACK.parent, cwd).replace('\\', '/')
    dur = end - start
    has_audio = ffprobe(video)['audio']
    vf = (f"[0:v]crop='min(iw,ih*9/16)':ih,scale={W}:{H},setsar=1,fps=30,"
          f"subtitles={ass.name}:fontsdir={fonts}[main];"
          f"[1:v]scale={W}:{H},setsar=1,fps=30,format=yuv420p[ec];")
    if has_audio:
        af = f"[0:a]aresample=48000,afade=t=out:st={dur - 0.3:.2f}:d=0.3[a0];"
    else:
        af = f"anullsrc=r=48000:cl=stereo,atrim=0:{dur:.2f}[a0];"
    fc = vf + af + f"anullsrc=r=48000:cl=stereo,atrim=0:2[a1];[main][a0][ec][a1]concat=n=2:v=1:a=1[v][a]"
    cmd = ['ffmpeg', '-y', '-v', 'error', '-ss', f'{start:.2f}', '-t', f'{dur:.2f}', '-i', str(Path(video).resolve()),
           '-loop', '1', '-t', '2', '-i', endcard_png.name, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '22', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
           '-b:a', '128k', '-movflags', '+faststart', out_mp4.name]
    subprocess.run(cmd, check=True, cwd=cwd)


def clip_meta(text, video_stem, n):
    first = re.split(r'(?<=[.!?])\s', text.strip())[0] if text else ''
    title = first.strip() or f'{video_stem.replace("_", " ").replace("-", " ").title()} — part {n}'
    if len(title) > 59:
        title = title[:56].rsplit(' ', 1)[0] + '…'
    desc = (f"{text.strip()}\n\nFull video on the channel. Shop sealed + slabs: https://www.hokocollectables.com\n"
            f"Collector first. Seller second.\n\n{' '.join(TAGS)}")
    return {'title': title, 'description': desc, 'hashtags': TAGS}


def run_inbox(model='small'):
    vids = sorted(INBOX.glob('*.mp4'))
    if not vids:
        print(f'No videos in {INBOX}')
        return []
    made = []
    for v in vids:
        od = OUT / v.stem
        od.mkdir(parents=True, exist_ok=True)
        ec = od / 'endcard.png'
        end_card().save(ec)
        segs = transcribe(v, model)
        dur = ffprobe(v)['duration']
        clips = pick_clips(segs, dur)
        print(f'{v.name}: {len(segs)} transcript segments, {len(clips)} clip(s)')
        for n, (score, a, b, text) in enumerate(clips, 1):
            ass = od / f'short_{n}.ass'
            write_ass(segs, a, b, ass)
            mp4 = od / f'short_{n}.mp4'
            cut_short(v, a, b, ass, mp4, ec)
            meta = clip_meta(' '.join(s['text'] for s in sentences(segs) if s['start'] >= a - 0.05 and s['end'] <= b + 0.05),
                             v.stem, n)
            meta.update({'source': v.name, 'start': round(a, 2), 'end': round(b, 2), 'hook_score': round(score, 2)})
            (od / f'short_{n}.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
            info = ffprobe(mp4)
            print(f"  short_{n}.mp4 {info['width']}x{info['height']} {info['duration']:.1f}s — {meta['title']}")
            made.append(mp4)
    return made


# ---------------------------------------------------------------- package

def title_variants(segs, stem):
    sents = [s['text'] for s in sentences(segs) if 4 <= len(s['text'].split()) <= 16]
    ranked = sorted(sents, key=hook_score, reverse=True)
    base = stem.replace('_', ' ').replace('-', ' ').title()
    out = []

    def add(t):
        if t and t not in out:
            out.append(t)
    add(ranked[0] if ranked else None)
    add(next((s for s in ranked if s.endswith('?') and s not in out), None) or f'Is {base} worth it?')
    add(next((s for s in ranked if re.search(r'\$?\d', s) and s not in out), None)
        or next((s for s in ranked if s not in out), None) or f'{base} — honest collector take')
    while len(out) < 3:
        out.append(f'{base} | HOKO Collectables')
    return [t if len(t) <= 70 else t[:67].rsplit(' ', 1)[0] + '…' for t in out[:3]]


def scene_frames(video, n=3):
    """Timestamps of the n strongest scene changes (ffmpeg scene score); evenly spaced fallback."""
    dur = ffprobe(video)['duration']
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(video), '-vf', "select='gt(scene,0.25)',showinfo",
                        '-an', '-f', 'null', '-'], capture_output=True, text=True)
    ts = [float(m) for m in re.findall(r'pts_time:([\d.]+)', r.stderr)]
    ts = [t for t in ts if 1 < t < dur - 1]
    picks = []
    for t in ts:
        if all(abs(t - p) > dur / (n * 2) for p in picks):
            picks.append(t)
        if len(picks) == n:
            break
    k = 1
    while len(picks) < n:
        picks.append(dur * k / (n + 1))
        k += 1
    return sorted(picks[:n])


def thumb(video, t, text, out_jpg):
    tmp = out_jpg.with_suffix('.png')
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{t:.2f}', '-i', str(video), '-frames:v', '1',
                    '-vf', 'scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720', str(tmp)], check=True)
    im = Image.open(tmp).convert('RGB')
    tmp.unlink()
    d = ImageDraw.Draw(im, 'RGBA')
    d.rectangle([0, 380, 1280, 720], fill=(0, 0, 0, 130))
    line = re.sub(r'[^\w$?!.,\' ]', '', text).upper()
    size = 112
    while True:
        f = font(size)
        lines = wrap(d, line, f, 1200)
        if len(lines) <= 2 or size <= 60:
            break
        size -= 6
    lines = lines[:2]
    y = 720 - 40 - len(lines) * int(size * 1.08)
    for ln in lines:
        tw = d.textlength(ln, font=f)
        d.text(((1280 - tw) / 2, y), ln, font=f, fill=(255, 255, 255), stroke_width=8, stroke_fill=(0, 0, 0))
        y += int(size * 1.08)
    tag = font(34)
    d.rounded_rectangle([30, 30, 60 + d.textlength('HOKO', font=tag), 86], 12, fill=(242, 193, 78, 255))
    d.text((45, 38), 'HOKO', font=tag, fill=(15, 15, 15))
    im.save(out_jpg, quality=90)


def package(video_arg, model='small'):
    v = Path(video_arg)
    if not v.exists():
        v = INBOX / video_arg
    if not v.exists():
        raise SystemExit(f'Video not found: {video_arg}')
    od = OUT / v.stem / 'package'
    od.mkdir(parents=True, exist_ok=True)
    segs = transcribe(v, model)
    titles = title_variants(segs, v.stem)
    times = scene_frames(v)
    for i, (t, ti) in enumerate(zip(times, titles), 1):
        thumb(v, t, ti, od / f'thumb_{i}.jpg')
    (od / 'titles.json').write_text(json.dumps({'titles': titles, 'thumb_times': times}, indent=2), encoding='utf-8')
    print(f'package {v.name}:')
    for t in titles:
        print('  title:', t)
    print(f'  thumbs: {", ".join(f"thumb_{i}.jpg" for i in range(1, 4))} @ {[round(x, 1) for x in times]}')
    return titles
