## Summary

v2.0.1 - The Intelligence & Stability Update, combining the massive feature drops of v2.0.0 and v2.0.1 into one stable package.

## What's New

- **Profile Intelligence Engine (v2.0.0)**: Introduced core JD awareness and deep Resume context. The AI dynamically adapts to the specific job description you are interviewing for.
- **Live Meeting RAG Integration**: Deep Retrieval-Augmented Generation directly into live meetings, pulling facts and context from your current and past history as the meeting unfolds.
- **Next-Gen Windows Audio Capture**: Re-engineered system audio selection for Windows, resolving WASAPI compatibility issues.
- **Soniox Speech Support**: Added the Soniox speech provider for high-accuracy, low-latency transcriptions.
- **Customizable Language Features**: Introduced custom AI response languages and speech languages.

## Improvements

- **Profile Engine UI Overhaul**: Radically redesigned the premium Profile Engine UI with a mature, Apple-like minimalist aesthetic, motion, and glassmorphism.
- **Apple Premium Dark Code Blocks**: Code snippets in the UI now render with a sleek Apple Premium Dark aesthetic, preserving critical whitespace.
- **Markdown Rendering**: Improved readability and stability across chat output via strict syntax highlighting.

## Fixes

- **Comprehensive Bug Fixes**: Resolved critical SQLite embedding indexing constraint errors, fixed ad-dismissal cooldowns, and handled dependency conflicts.
- **Production Enhancements**: Fixed Native module compilation and packaging for smoother application delivery, alongside adding correct Windows build icons.

## Technical

- **Merged PR Integrations**: Successfully merged 3 major pull requests, streamlining repository contributions.

## ⚠️macOS Installation (Unsigned Build)

Download the correct architecture .zip or .dmg file for your device (Apple Silicon or Intel).

If you see "App is damaged":

- **For .zip downloads:**
  1. Move the app to your Applications folder.
  2. Open Terminal and run: `xattr -cr /Applications/Natively.app`

- **For .dmg downloads:**
  1. Open Terminal and run:
     ```bash
     xattr -cr ~/Downloads/Natively-1.1.8-arm64.dmg
     ```
  2. Install the natively.dmg
  3. Open Terminal and run: `xattr -cr /Applications/Natively.app`
