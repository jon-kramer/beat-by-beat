# Beat by Beat - Quick Start

## First Time

```bash
# 1. Install dependencies
./setup.sh

# 2. Generate cards
uv run python card-generator/generator.py

# 3. View in browser
open output/index.html
```

## After Editing CSVs

```bash
./generate-all.sh
```

This regenerates HTML, PDF, and TTS files.

## Individual Formats

```bash
# HTML only
uv run python card-generator/generator.py

# PDF only
uv run python card-generator/pdf_generator.py

# TTS sprites only
uv run python card-generator/tts_generator.py
```

## What Gets Generated

| Format | Location | Use For |
|--------|----------|---------|
| HTML | `output/` | Browser printing, preview |
| PDF | `pdf/` | Print shops, physical cards |
| TTS | `tts/` | Tabletop Simulator online play |

## Dependencies

Managed by `uv` via `pyproject.toml`:
- **Playwright** - PDF generation (auto-installs Chromium)
- **Pillow** - TTS sprite sheet generation

Run `./setup.sh` once to install everything.

## More Info

- **README.md** - Full documentation
- **PDF-AND-TTS-GUIDE.md** - Detailed PDF/TTS instructions
- **COMMAND-REFERENCE.md** - All commands
- **PRINTING-GUIDE.md** - How to print cards
