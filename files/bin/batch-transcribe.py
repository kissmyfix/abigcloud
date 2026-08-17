import sys
import time
import os
from faster_whisper import WhisperModel

queue_path = sys.argv[1]
mp3_dir = sys.argv[2]
out_dir = sys.argv[3]

with open(queue_path) as f:
    filenames = [line.rstrip("\n") for line in f if line.strip()]

model = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=4)

def fmt_ts(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"

for idx, fname in enumerate(filenames, 1):
    src = os.path.join(mp3_dir, fname)
    base = os.path.splitext(fname)[0]
    out_path = os.path.join(out_dir, base + ".txt")

    if os.path.exists(out_path):
        print(f"[{idx}/{len(filenames)}] SKIP (already done): {fname}", flush=True)
        continue

    print(f"[{idx}/{len(filenames)}] START: {fname}", flush=True)
    start = time.time()
    segments, info = model.transcribe(src, beam_size=5, vad_filter=True, word_timestamps=False)
    print(f"  duration={info.duration:.1f}s language={info.language}", flush=True)

    with open(out_path, "w") as out:
        for seg in segments:
            line = f"[{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}] {seg.text.strip()}\n"
            out.write(line)
            out.flush()

    elapsed = time.time() - start
    print(f"[{idx}/{len(filenames)}] DONE in {elapsed:.0f}s: {fname}", flush=True)

print("ALL DONE", flush=True)
