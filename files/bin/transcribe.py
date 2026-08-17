import sys
import time
from faster_whisper import WhisperModel

audio_path = sys.argv[1]
out_path = sys.argv[2]

model = WhisperModel("medium.en", device="cpu", compute_type="int8", cpu_threads=4)

start = time.time()
segments, info = model.transcribe(
    audio_path,
    beam_size=5,
    vad_filter=True,
    word_timestamps=False,
)

print(f"Detected language: {info.language} (p={info.language_probability:.2f})", flush=True)
print(f"Duration: {info.duration:.1f}s", flush=True)

def fmt_ts(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:05.2f}"

with open(out_path, "w") as f:
    for seg in segments:
        line = f"[{fmt_ts(seg.start)} --> {fmt_ts(seg.end)}] {seg.text.strip()}\n"
        f.write(line)
        f.flush()
        elapsed = time.time() - start
        print(f"{fmt_ts(seg.end)} (elapsed {elapsed:.0f}s)", flush=True)

print(f"Done in {time.time()-start:.0f}s", flush=True)
