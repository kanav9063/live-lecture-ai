## Summary

The Intelligence & Stability Update, bringing Live RAG, Soniox support, and a completely overhauled UI.

## What's New

- Live Meeting RAG Integration for instantly pulling facts from past meetings.
- Soniox speech provider for high-accuracy, low-latency transcriptions.
- Customizable AI response languages and speech languages.

## Improvements

- Radically redesigned Profile Engine UI with a mature Apple-like minimalist aesthetic and glassmorphism.
- Introduced Apple Premium Dark aesthetic for code blocks to preserve critical whitespace.
- Re-engineered Windows audio capture resolving WASAPI compatibility issues.
- Improved Markdown readability and stability across chat output via strict syntax highlighting.

## Fixes

- Resolved critical SQLite embedding indexing constraint errors.
- Fixed ad-dismissal cooldowns to properly track hidden states.
- Handled React dependency conflicts related to async-storage.
- Fixed Native module compilation and packaging for smoother delivery on Windows.

## Technical

- Merged 3 major PRs streamlining repository contributions.
- Added correct Windows build icons.

## ⚠️macOS Installation (Unsigned Build)

Download the correct architecture .zip or .dmg file for your device (Apple Silicon or Intel).

If you see "App is damaged":

- **For .zip downloads:**
  1. Move the app to your Applications folder.
  2. Open Terminal and run: `xattr -cr /Applications/Natively.app`

- **For .dmg downloads:**
  1. Open Terminal and run:
     ```bash
     xattr -cr ~/Downloads/Natively-2.0.1-arm64.dmg
     ```
  2. Install the natively.dmg
  3. Open Terminal and run: `xattr -cr /Applications/Natively.app`
