# Beat by Beat - Card Generator

A printable card generation system for the Beat by Beat dance-themed deck builder game.

## Overview

This system generates print-ready HTML files for all game cards, designed for standard 8.5×11" paper with 9 poker-sized cards (2.5" × 3.5") per sheet.

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

## Directory Structure

```
beat-by-beat/
├── card-data/          # CSV files with card data
│   ├── moves.csv
│   ├── rhythm-cards.csv
│   ├── judge-cards.csv
│   └── stumble-cards.csv
├── card-generator/     # Generation scripts
│   └── generator.py
├── output/            # Generated HTML files
│   ├── index.html            # Card browser
│   ├── move-cards.html       # All 170 move cards (19 sheets)
│   ├── rhythm-cards.html     # All 80 rhythm cards (9 sheets)
│   ├── judge-cards.html      # All 12 judge cards (2 sheets)
│   ├── stumble-cards.html    # All 20 stumble cards (3 sheets)
│   └── [card-type]-backs.html (for each card type)
├── images/            # Future: custom card artwork
└── docs/              # Game documentation
```

## Usage

### Generating Cards

```bash
python3 card-generator/generator.py
```

This will regenerate all HTML files in the `output/` directory.

### Printing Cards

1. Open `output/index.html` in your web browser
2. Click on the card type you want to print (e.g., "Move Cards")
3. Use Print (Cmd+P or Ctrl+P)
4. Settings:
   - Paper size: Letter (8.5×11")
   - Margins: None
   - Scale: 100%
   - Background graphics: On
5. Print or save as PDF - all sheets will print together!

### Printing Double-Sided Cards

For cards with backs:

1. Print all front sheets (e.g., `move-cards.html` - prints all 19 sheets)
2. Flip the paper stack (check orientation with a test print)
3. Print the back file (e.g., `move-backs.html`) - repeat as needed for the number of sheets

**Note**: All backs are identical for each card type, so you print the same back design on each sheet.

## Customization

### Editing Card Data

All card data is stored in CSV files in `card-data/`. Edit these files and re-run the generator to update the cards.

### Adding Custom Artwork

The system is designed to support custom vector images:

1. Create SVG files for each card (filenames match the `image_file` column in CSV)
2. Place them in the `images/` directory
3. Update `generator.py` to use actual image files instead of placeholder SVG icons

Current placeholder graphics:
- **Type icons**: Simple geometric shapes representing each movement type (Step, Spin, Jump, Pose, Flow, Pop)
- **Color backgrounds**: Style-specific colors with gradients for multi-style cards

### Modifying Card Design

The card layout and styling is defined in the `generate_css()` function in `generator.py`. You can customize:

- Fonts and sizes
- Colors and backgrounds
- Layout and spacing
- Border styles

## Card Counts

| Card Type | Count | Sheets (9/sheet) | HTML File |
|-----------|-------|------------------|-----------|
| Move Cards | 170 | 19 sheets | `move-cards.html` |
| Rhythm Cards | 80 | 9 sheets | `rhythm-cards.html` |
| Judge Cards | 12 | 2 sheets | `judge-cards.html` |
| Stumble Cards | 20 | 3 sheets | `stumble-cards.html` |
| **Total** | **282** | **33 sheets** | **4 files** |

Plus 4 back files (one per card type). Each HTML file contains all sheets for that card type.

## Setup

First-time setup (installs all dependencies):

```bash
./setup.sh
```

This installs Python dependencies via `uv` and Playwright's Chromium browser.

## Advanced Features

### Automated PDF Generation

Generate print-ready PDFs without using your browser:

```bash
uv run python card-generator/pdf_generator.py
```

PDFs are created in the `pdf/` directory.

### Tabletop Simulator Export

Generate sprite sheets for online play:

```bash
uv run python card-generator/tts_generator.py
```

Creates 10×7 sprite sheets in the `tts/` directory.

See [PDF-AND-TTS-GUIDE.md](PDF-AND-TTS-GUIDE.md) for detailed instructions.

### Generate Everything

```bash
./generate-all.sh
```

Generates HTML, PDF, and TTS formats in one command!

## Future Enhancements

- [x] Generate PDF output directly
- [x] Tabletop Simulator sprite sheets
- [ ] Add unique vector illustrations for each card
- [ ] Add bleed lines for professional printing
- [ ] Create card sorting/organizing sheets
- [ ] Add QR codes linking to online rulebook
- [ ] Token/counter sheets
- [ ] Player aid cards
- [ ] Automated TTS JSON deck configuration
- [ ] Direct image upload to Imgur

## Credits

Game design and card data extracted from documentation in `docs/`.

Color scheme: Coral, Indigo, Sage, Gold, and Slate Blue palette.
