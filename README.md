# Beat by Beat

A competitive dance-battle card game where players choreograph routines, impress judges, and battle for the spotlight.

## Overview

Beat by Beat is a deck-building card game where 2-5 players compete as dancers trying to impress various judges. Players build their routines from Move cards, adapt to Rhythm cards, and avoid Stumbles while trying to meet Judge requirements.

This repository contains a complete card generation system that produces:
- **HTML** printable sheets (3×3 cards per letter-size page)
- **PDF** print-ready files for professional printing
- **TTS** high-resolution sprite sheets for Tabletop Simulator

## Generated Cards

- **Move Cards**: 170 total (50 starter deck cards for 5 players + 120 common pool cards)
- **Rhythm Cards**: 80 cards
- **Judge Cards**: 12 cards
- **Stumble Cards**: 20 cards
- **Card Backs**: Designs for each card type

## Color Scheme

Each dance style has a unique thematic color:

- **Latin** (passionate, rhythmic): Coral `#FF6B6B`
- **Ballroom** (elegant, refined): Deep Indigo `#6B5B95`
- **Classical** (graceful, technical): Soft Sage `#8FB996`
- **Jazz** (theatrical, energetic): Warm Gold `#E9C46A`
- **Street** (urban, dynamic): Slate Blue `#457B9D`
- **Styleless** (starter deck): Cream `#FAF8F3`
- **Multi-style**: Gradient blending both style colors

## Quick Start

### Setup

First-time setup (installs all dependencies):

```bash
./scripts/setup.sh
```

### Generate All Cards

Generate HTML, PDF, and TTS formats in one command:

```bash
./scripts/generate-all.sh
```

Output locations:
- HTML: `output/html/`
- PDF: `output/pdf/`
- TTS: `output/tts/`

### Publish to Tabletop Simulator

```bash
./scripts/publish-tts.sh
```

This generates TTS sprites, commits them to git, pushes to GitHub, and displays the raw URLs for importing into Tabletop Simulator.

## Directory Structure

```
beat-by-beat/
├── card-data/           # CSV files with card definitions
│   ├── moves.csv
│   ├── rhythm-cards.csv
│   ├── judge-cards.csv
│   └── stumble-cards.csv
├── card-generator/      # Python generators
│   ├── generator.py     # HTML generator
│   ├── pdf_generator.py # PDF generator
│   └── tts_generator.py # TTS sprite sheet generator
├── output/             # Generated files
│   ├── html/          # HTML printable sheets
│   ├── pdf/           # Print-ready PDFs
│   └── tts/           # TTS sprite sheets (4096×4096)
├── scripts/           # Utility scripts
│   ├── setup.sh
│   ├── generate-all.sh
│   ├── publish-tts.sh
│   └── get-tts-urls.sh
└── docs/              # Documentation
```

## Card Types

### Move Cards
The core of your dance routine. Each move has:
- **Cost**: Energy required to perform
- **Type**: Step, Spin, Jump, Pose, Flow, or Pop
- **Style**: Latin, Ballroom, Classical, Jazz, or Street
- **Bonus**: Points awarded for successful execution

### Rhythm Cards
Modify gameplay each round with special effects or provide blank cards for freestyle.

### Judge Cards
Win conditions that award points for meeting specific requirements (style combinations, move types, etc.).

### Stumble Cards
Penalty cards that clog your hand when you fail a move.

## Printing Cards

### Using HTML Files

1. Open HTML files in `output/html/` in your web browser
2. Use Print (Cmd+P or Ctrl+P)
3. Settings:
   - Paper size: Letter (8.5×11")
   - Margins: None
   - Scale: 100%
   - Background graphics: On
4. Print or save as PDF

### Using PDF Files

Open files in `output/pdf/` and print directly. Perfect for print shops.

### Double-Sided Printing

For cards with backs:

1. Print all front sheets (e.g., `move-cards.pdf`)
2. Flip the paper stack (check orientation with a test print)
3. Print the back file (e.g., `move-backs.pdf`) - repeat as needed

**Note**: All backs are identical for each card type.

## Development

### Modifying Cards

1. Edit the CSV files in `card-data/`
2. Run `./scripts/generate-all.sh` to regenerate all formats
3. Check `output/` directories for results

### Card Data Format

See CSV files in `card-data/` for examples. Key fields:

**moves.csv:**
- name, cost, type, style, bonus, deck_type

**rhythm-cards.csv:**
- name, effect, condition, flavor_text, copies

**judge-cards.csv:**
- name, title, difficulty, requirement, reward_points, ongoing_effect

### Technical Details

- **HTML/CSS**: Cards designed at 2.5" × 3.5" (poker size)
- **TTS Rendering**: Uses Playwright to render HTML directly into sprite sheets
- **Consistency**: All formats share the same HTML/CSS source for perfect visual consistency

See [docs/TTS-RENDERING.md](docs/TTS-RENDERING.md) for detailed technical documentation.

## Card Counts

| Card Type | Count | Sheets (9/sheet) | HTML File |
|-----------|-------|------------------|-----------|
| Move Cards | 170 | 19 sheets | `move-cards.html` |
| Rhythm Cards | 80 | 9 sheets | `rhythm-cards.html` |
| Judge Cards | 12 | 2 sheets | `judge-cards.html` |
| Stumble Cards | 20 | 3 sheets | `stumble-cards.html` |
| **Total** | **282** | **33 sheets** | **4 files** |

Plus 4 back files (one per card type). Each HTML file contains all sheets for that card type.

## Scripts Reference

- `./scripts/setup.sh` - Install dependencies (Python, uv, Playwright)
- `./scripts/generate-all.sh` - Generate all card formats
- `./scripts/publish-tts.sh` - Generate and publish TTS sprites to GitHub
- `./scripts/get-tts-urls.sh` - Display GitHub raw URLs for TTS import

## Documentation

Detailed guides available in the `docs/` directory:

- **[docs/PRINTING.md](docs/PRINTING.md)** - Complete printing guide with paper recommendations, cutting tips, and troubleshooting
- **[docs/TTS-RENDERING.md](docs/TTS-RENDERING.md)** - Technical details on TTS sprite sheet generation and HTML rendering
- **[docs/TTS-GITHUB.md](docs/TTS-GITHUB.md)** - How to host TTS sprites on GitHub for free, permanent URLs
- **[docs/GITHUB-SETUP.md](docs/GITHUB-SETUP.md)** - Step-by-step GitHub setup for TTS hosting

## Requirements

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (Python package manager)
- Playwright (automatically installed by setup)

## License

[Add your license here]

## Contributing

[Add contribution guidelines if applicable]
