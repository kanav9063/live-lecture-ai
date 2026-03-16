"""
Live Lecture AI — Real-time transcription + AI Q&A

Modes:
  1. FILE MODE:  Transcribe a video/audio file in streaming chunks, then ask questions
  2. LIVE MODE:  Capture system audio in real time (macOS/Linux), transcribe + Q&A

Usage:
  python transcriber.py --file lecture.mp4          # transcribe a file
  python transcriber.py --file lecture.mp4 --chat    # transcribe + interactive Q&A
  python transcriber.py --live                       # live mic capture + Q&A
  python transcriber.py --live --device 1            # specific audio device
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

# ── Transcription engine ─────────────────────────────────────────────
class Transcriber:
    def __init__(self, model_size="base", device="cpu", compute_type="int8"):
        from faster_whisper import WhisperModel
        print(f"[init] Loading Whisper model '{model_size}' on {device}...")
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("[init] Model loaded ✓")

    def transcribe_chunk(self, audio_path):
        """Transcribe a single audio chunk, return text."""
        segments, info = self.model.transcribe(audio_path, beam_size=5, language="en")
        texts = []
        for seg in segments:
            texts.append(seg.text.strip())
        return " ".join(texts)


# ── AI Q&A engine ────────────────────────────────────────────────────
class LectureAI:
    def __init__(self, model="gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model
        self.transcript_lines = []
        self.lock = threading.Lock()

    def add_transcript(self, text, timestamp=None):
        with self.lock:
            prefix = f"[{timestamp}] " if timestamp else ""
            self.transcript_lines.append(f"{prefix}{text}")

    def get_full_transcript(self):
        with self.lock:
            return "\n".join(self.transcript_lines)

    def ask(self, question):
        transcript = self.get_full_transcript()
        if not transcript.strip():
            return "No transcript available yet."

        # Trim to last ~12000 chars to fit context
        if len(transcript) > 12000:
            transcript = "...\n" + transcript[-12000:]

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant helping a student understand a live lecture. "
                        "Below is the running transcript of what the professor is saying. "
                        "Answer the student's question based ONLY on what's in the transcript. "
                        "Be concise and helpful. If the transcript doesn't cover the question, say so.\n\n"
                        f"=== LECTURE TRANSCRIPT ===\n{transcript}\n=== END TRANSCRIPT ==="
                    )
                },
                {"role": "user", "content": question}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content

    def auto_summarize(self):
        """Generate a quick summary of the transcript so far."""
        return self.ask("Give me a concise summary of what's been covered so far in this lecture.")


# ── File mode: chunk a video/audio file and transcribe ───────────────
def extract_audio_chunks(filepath, chunk_seconds=30):
    """Use ffmpeg to split audio into chunks. Yields (chunk_path, start_time)."""
    # Get duration
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "json", filepath],
        capture_output=True, text=True
    )
    duration = float(json.loads(result.stdout)["format"]["duration"])

    tmpdir = tempfile.mkdtemp(prefix="lecture_ai_")
    start = 0.0
    chunk_idx = 0

    while start < duration:
        chunk_path = os.path.join(tmpdir, f"chunk_{chunk_idx:04d}.wav")
        subprocess.run(
            ["ffmpeg", "-y", "-i", filepath, "-ss", str(start),
             "-t", str(chunk_seconds), "-ar", "16000", "-ac", "1",
             "-f", "wav", chunk_path],
            capture_output=True
        )
        if os.path.exists(chunk_path) and os.path.getsize(chunk_path) > 1000:
            mins = int(start // 60)
            secs = int(start % 60)
            yield chunk_path, f"{mins:02d}:{secs:02d}"
        start += chunk_seconds
        chunk_idx += 1


def run_file_mode(filepath, chat_mode=False, model_size="base"):
    transcriber = Transcriber(model_size=model_size)
    ai = LectureAI()

    print(f"\n[transcribe] Processing: {filepath}")
    print("─" * 60)

    for chunk_path, timestamp in extract_audio_chunks(filepath):
        text = transcriber.transcribe_chunk(chunk_path)
        if text.strip():
            ai.add_transcript(text, timestamp)
            print(f"  [{timestamp}] {text}")
        os.unlink(chunk_path)

    print("─" * 60)
    print("[transcribe] Done!\n")

    # Save transcript
    transcript = ai.get_full_transcript()
    out_path = Path(filepath).stem + "_transcript.txt"
    with open(out_path, "w") as f:
        f.write(transcript)
    print(f"[saved] Transcript → {out_path}")

    if chat_mode:
        print("\n💬 Chat mode — ask questions about the lecture (type 'quit' to exit, 'summary' for summary)")
        print("─" * 60)
        while True:
            try:
                q = input("\n❓ You: ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not q:
                continue
            if q.lower() in ("quit", "exit", "q"):
                break
            if q.lower() == "summary":
                print(f"\n📋 {ai.auto_summarize()}")
                continue
            answer = ai.ask(q)
            print(f"\n🤖 {answer}")
    else:
        # Auto-generate summary
        print(f"\n📋 Summary:\n{ai.auto_summarize()}")

    return ai


# ── Live mode: capture mic/system audio in real time ─────────────────
def run_live_mode(device_index=None, model_size="base"):
    try:
        import pyaudio
    except ImportError:
        print("ERROR: pyaudio not installed. Run: pip install pyaudio")
        print("  macOS: brew install portaudio && pip install pyaudio")
        sys.exit(1)

    transcriber = Transcriber(model_size=model_size)
    ai = LectureAI()
    pa = pyaudio.PyAudio()

    # List devices if needed
    if device_index is None:
        print("\n🎤 Available audio devices:")
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            if info["maxInputChannels"] > 0:
                print(f"  [{i}] {info['name']} (in:{info['maxInputChannels']})")
        device_index = int(input("\nSelect device index: "))

    dev_info = pa.get_device_info_by_index(device_index)
    sample_rate = int(dev_info["defaultSampleRate"])
    channels = min(dev_info["maxInputChannels"], 1)

    print(f"\n[live] Listening on: {dev_info['name']}")
    print("[live] Transcribing... (Ctrl+C to stop, type questions in terminal)")
    print("─" * 60)

    # Audio capture thread
    CHUNK_DURATION = 5  # seconds per transcription chunk
    frames = []
    recording = True

    def audio_callback(in_data, frame_count, time_info, status):
        if recording:
            frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    stream = pa.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        input_device_index=device_index,
        frames_per_buffer=1024,
        stream_callback=audio_callback
    )
    stream.start_stream()

    start_time = time.time()

    def transcription_loop():
        import wave
        nonlocal frames
        while recording:
            time.sleep(CHUNK_DURATION)
            if not frames:
                continue

            # Grab current frames and reset
            current_frames = frames[:]
            frames = []

            # Write to temp wav
            fd, tmp_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd)
            try:
                with wave.open(tmp_path, "wb") as wf:
                    wf.setnchannels(channels)
                    wf.setsampwidth(2)  # 16-bit
                    wf.setframerate(sample_rate)
                    wf.writeframes(b"".join(current_frames))

                text = transcriber.transcribe_chunk(tmp_path)
                if text.strip():
                    elapsed = time.time() - start_time
                    mins = int(elapsed // 60)
                    secs = int(elapsed % 60)
                    ts = f"{mins:02d}:{secs:02d}"
                    ai.add_transcript(text, ts)
                    print(f"  [{ts}] {text}")
            finally:
                os.unlink(tmp_path)

    t = threading.Thread(target=transcription_loop, daemon=True)
    t.start()

    # Q&A loop in main thread
    print("\n💬 Type questions anytime (or 'summary', 'transcript', 'quit'):\n")
    try:
        while True:
            q = input("❓ ").strip()
            if not q:
                continue
            if q.lower() in ("quit", "exit", "q"):
                break
            if q.lower() == "summary":
                print(f"\n📋 {ai.auto_summarize()}\n")
                continue
            if q.lower() == "transcript":
                print(f"\n📝 {ai.get_full_transcript()}\n")
                continue
            answer = ai.ask(q)
            print(f"\n🤖 {answer}\n")
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        recording = False
        stream.stop_stream()
        stream.close()
        pa.terminate()

        # Save transcript
        transcript = ai.get_full_transcript()
        if transcript.strip():
            out_path = "live_transcript.txt"
            with open(out_path, "w") as f:
                f.write(transcript)
            print(f"\n[saved] Transcript → {out_path}")


# ── CLI ──────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Live Lecture AI — Real-time transcription + Q&A")
    parser.add_argument("--file", type=str, help="Path to video/audio file")
    parser.add_argument("--live", action="store_true", help="Live mic/system audio capture")
    parser.add_argument("--chat", action="store_true", help="Interactive Q&A after transcription")
    parser.add_argument("--device", type=int, default=None, help="Audio device index for live mode")
    parser.add_argument("--model", type=str, default="base", help="Whisper model size (tiny/base/small/medium/large-v3)")
    args = parser.parse_args()

    if not args.file and not args.live:
        parser.print_help()
        print("\nExample:")
        print("  python transcriber.py --file lecture.mp4 --chat")
        print("  python transcriber.py --live")
        sys.exit(1)

    if args.file:
        run_file_mode(args.file, chat_mode=args.chat, model_size=args.model)
    elif args.live:
        run_live_mode(device_index=args.device, model_size=args.model)


if __name__ == "__main__":
    main()
