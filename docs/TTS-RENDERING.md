# TTS Rendering Approach

## Overview

The TTS (Tabletop Simulator) sprite sheets are generated using **HTML rendering via Playwright** instead of direct pixel drawing with PIL. This ensures perfect consistency across all output formats.

## How It Works

### Generation Pipeline

1. **HTML cards** are generated first (`card-generator/generator.py`)
2. **Playwright** renders each HTML card as a high-resolution screenshot
3. **PIL** resizes and assembles the screenshots into 10×7 sprite sheet grids

### Why This Approach?

**Benefits:**
- ✅ Perfect visual consistency between HTML, PDF, and TTS
- ✅ Single source of truth for card design (HTML/CSS)
- ✅ Easier maintenance - update HTML once, affects all formats
- ✅ Professional rendering with proper fonts, colors, and layout
- ✅ No need to manually replicate CSS styling in Python

**Trade-offs:**
- Slightly slower generation (requires browser rendering)
- Requires Playwright/Chromium (already needed for PDFs)

## Files

- **tts_generator.py** - HTML-based TTS generator (uses Playwright)

## Usage

The generator is automatically used by `./scripts/generate-all.sh`:

```bash
# Generate all formats including TTS
./scripts/generate-all.sh

# Or generate TTS only
uv run python card-generator/tts_generator.py
```

## Technical Details

### Card Rendering

Each card is rendered at **750×1050 pixels** (2.5" × 3.5" at 300 DPI), then:
1. Resized to fit TTS grid cell dimensions (204-205 × 292-293 pixels)
2. Positioned in exact grid locations to avoid gaps/overlaps

### Sprite Sheet Specs

- **Resolution**: 2048×2048 pixels
- **Grid**: 10 cards wide × 7 cards tall
- **Cards per sheet**: 70
- **Format**: PNG with optimization

### Card Extraction

The generator:
1. Loads each HTML file (e.g., `move-cards.html`)
2. Extracts all `.card` elements (excluding `.card-back`)
3. Renders each card individually with proper CSS
4. Assembles them into sprite sheets

### Card Backs

Card backs are rendered once per type and duplicated across the sheet for efficiency.

## Consistency Guarantee

Because TTS sprites are rendered from the **exact same HTML/CSS** as the printable cards:
- Colors match perfectly
- Fonts are identical
- Layout is consistent
- Any design changes automatically propagate to all formats

## Future Improvements

Possible enhancements:
- Cache rendered cards to speed up regeneration
- Support higher resolution (4096×4096) with a flag
- Parallel rendering for faster generation
