# 🎓 Lecture Mode — Live Lecture AI

This fork adds **Lecture Mode** to Natively — optimized for sitting in class and getting real-time AI assistance based on what the professor is saying.

## What's Different from Interview Mode?

| Feature | Interview Mode (Original) | Lecture Mode (New) |
|---------|--------------------------|-------------------|
| **Purpose** | Generate what YOU should say | Help you UNDERSTAND what's being said |
| **AI Role** | Interview copilot | Study companion |
| **Context** | Interview Q&A | Lecture transcript |
| **Output** | Spoken answers | Explanations, notes, Q&A |

## Lecture Mode Features

### 🎤 Real-Time Transcription
- Captures professor's audio via mic or system audio
- Streams transcription using Deepgram/Google/Soniox (same as base)
- Rolling transcript maintained in memory

### 💬 Ask Questions About the Lecture
- "What did they mean by X?"
- "Explain that last part simpler"  
- "How does X relate to Y they mentioned earlier?"
- "Give me the key formula"
- "Summarize the last 5 minutes"

### 📝 Auto Study Notes
- Generates structured notes from the lecture
- Key concepts, formulas, connections
- Questions to review later

### 🧠 Smart Context
- AI answers are grounded ONLY in what the professor actually said
- References earlier parts of the lecture when relevant
- Tells you when the professor hasn't covered something yet

## Setup

Same as base Natively — see [README.md](README.md)

1. Download the release for your OS
2. Add your API keys (OpenAI, Anthropic, Google, or Deepgram)
3. Select Lecture Mode from the mode dropdown
4. Start capturing audio
5. Ask questions in the overlay

## Architecture

```
Professor's Audio
    │
    ▼
┌─────────────────────┐
│ System Audio Capture │  ← Natively's native audio module
└──────────┬──────────┘
           │ raw PCM stream
           ▼
┌─────────────────────┐
│ Streaming STT        │  ← Deepgram Nova-2 / Google / Soniox
│ (sub-300ms latency)  │
└──────────┬──────────┘
           │ text chunks
           ▼
┌─────────────────────┐
│ Rolling Transcript   │  ← SessionTracker
│ + Temporal Context   │
└──────────┬──────────┘
           │ full context
           ▼
┌─────────────────────┐
│ LectureLLM           │  ← NEW: Lecture-specific prompts
│ (GPT/Claude/Gemini)  │     Q&A, notes, explanations
└─────────────────────┘
```

## New Files

- `electron/llm/LectureLLM.ts` — Lecture mode prompts + handlers
- `LECTURE_MODE.md` — This file

## Credits

- Base: [Natively](https://github.com/evinjohnn/natively-cluely-ai-assistant) by Evin John
- Lecture Mode: Added by Kanav Arora
