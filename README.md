# 🎓 Live Lecture AI

Real-time lecture transcription + AI Q&A assistant. Transcribes what your professor says and lets you ask questions about it — live.

## Demo

```
$ python transcriber.py --file lecture.mp4 --chat

[transcribe] Processing: lecture.mp4
──────────────────────────────────────────────────────
  [00:00] Today we're going to talk about gradient descent...
  [00:30] The key insight is that we move in the direction of steepest descent...
  [01:00] Learning rate determines how big each step is...
──────────────────────────────────────────────────────
[transcribe] Done!

💬 Chat mode — ask questions about the lecture

❓ You: What determines step size?

🤖 According to the lecture, the learning rate determines how big each step is
   in gradient descent.
```

## Quick Start

### 1. Install

```bash
# Clone
git clone https://github.com/kanav9063/live-lecture-ai.git
cd live-lecture-ai

# Install deps
pip install -r requirements.txt

# For live mode on macOS:
brew install portaudio
pip install pyaudio
```

### 2. Set OpenAI key

```bash
export OPENAI_API_KEY="your-key-here"
```

### 3. Run

**Transcribe a recorded lecture + ask questions:**
```bash
python transcriber.py --file lecture.mp4 --chat
```

**Live mode — listen to your mic in real time:**
```bash
python transcriber.py --live
```

**Just transcribe (no Q&A):**
```bash
python transcriber.py --file lecture.mp4
```

## Options

| Flag | Description |
|------|-------------|
| `--file <path>` | Path to video/audio file |
| `--live` | Live mic/system audio capture |
| `--chat` | Interactive Q&A mode after transcription |
| `--device <n>` | Audio device index for live mode |
| `--model <size>` | Whisper model: `tiny`, `base`, `small`, `medium`, `large-v3` |

## How It Works

1. **Transcription**: Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2-optimized Whisper) to transcribe audio in real-time chunks
2. **AI Q&A**: Feeds the running transcript to GPT-4o-mini as context, so you can ask questions about what's been said
3. **Live mode**: Captures system audio, transcribes in 5-second chunks, lets you type questions while listening

## Architecture

```
Audio Input (file/mic)
    │
    ▼
┌─────────────────┐
│  ffmpeg/pyaudio  │  ← audio capture
└────────┬────────┘
         │ chunks (5-30s WAV)
         ▼
┌─────────────────┐
│  faster-whisper  │  ← local STT (no cloud)
└────────┬────────┘
         │ text
         ▼
┌─────────────────┐
│  Rolling Transcript │
└────────┬────────┘
         │ context
         ▼
┌─────────────────┐
│   GPT-4o-mini   │  ← Q&A engine
└─────────────────┘
```

## Tips for Class Use

- **Use `--model small` or `--model medium`** for better accuracy (needs more RAM/GPU)
- **`base` is the default** — fast, works on CPU, good enough for clear audio
- **Live mode on macOS**: Use BlackHole or Soundflower to capture system audio (not just mic)
- The transcript auto-saves to `{filename}_transcript.txt` or `live_transcript.txt`

## Requirements

- Python 3.8+
- ffmpeg (for file mode)
- portaudio (for live mode on macOS)
- OpenAI API key (for Q&A — transcription is 100% local)

## License

MIT
