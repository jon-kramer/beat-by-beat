# Beat by Beat - PDF & Tabletop Simulator Guide

## 📄 Automated PDF Generation

### First Time Setup

Install Playwright's Chromium browser (one-time, ~100MB download):

```bash
uv run --with playwright playwright install chromium
```

### Generate PDFs

```bash
uv run --with playwright python card-generator/pdf_generator.py
```

The `--with playwright` flag tells `uv` to automatically install the Playwright Python package if needed.

This creates print-ready PDFs in the `pdf/` directory:
- `move-cards.pdf` (19 pages)
- `rhythm-cards.pdf` (9 pages)
- `judge-cards.pdf` (2 pages)
- `stumble-cards.pdf` (3 pages)
- Plus 4 back files

### Advantages

- **Automated**: No manual browser printing needed
- **Consistent**: Exact same output every time
- **Batch**: Generate all PDFs with one command
- **Professional**: Ready to send to print shops

### Print Settings

The PDFs are pre-configured with:
- Letter size (8.5" × 11")
- No margins
- Background graphics enabled
- Proper page breaks

Just open and print!

---

## 🎮 Tabletop Simulator Export

### What is TTS Format?

Tabletop Simulator uses sprite sheets:
- 10 cards wide × 7 cards tall = 70 cards per sheet
- 2048×2048 pixel PNG images
- Separate images for fronts and backs

### Generate TTS Sprite Sheets

```bash
uv run --with Pillow python card-generator/tts_generator.py
```

The `--with Pillow` flag tells `uv` to automatically install the Pillow package if needed.

This creates PNG sprite sheets in the `tts/` directory:
- `move-cards_1.png`, `move-cards_2.png`, etc.
- `move-backs.png`
- `rhythm-cards_1.png`, `rhythm-cards_2.png`
- `rhythm-backs.png`
- `judge-cards.png`
- `judge-backs.png`
- `stumble-cards.png`
- `stumble-backs.png`

### Import into Tabletop Simulator

#### Step 1: Upload Images

Upload the PNG files to an image hosting service:
- **Imgur** (recommended - free, TTS-friendly)
- **Google Drive** (make sure sharing is public)
- **Dropbox** or similar

Copy the direct image URLs.

#### Step 2: Create Custom Deck in TTS

1. In Tabletop Simulator, click **Objects** → **Components** → **Custom** → **Deck**
2. In the dialog:
   - **Face**: Paste URL to card fronts (e.g., `move-cards_1.png`)
   - **Back**: Paste URL to card backs (e.g., `move-backs.png`)
   - **Width**: `10`
   - **Height**: `7`
   - **Number**: Number of cards in that sheet (e.g., 70 for full sheet, less for partial)
   - **Unique Backs**: No (all backs are identical)

3. Click **Import**

#### Step 3: Repeat for Each Deck

Create separate decks for:
- Move cards (needs 3 decks for 170 cards: 70 + 70 + 30)
- Rhythm cards (needs 2 decks for 80 cards: 70 + 10)
- Judge cards (1 deck, 12 cards)
- Stumble cards (1 deck, 20 cards)

### TTS Deck Configuration

For a complete game setup, you'll create:

| Deck | Sprite Sheets | Cards | TTS Decks Needed |
|------|---------------|-------|------------------|
| Move Cards | 3 sheets | 170 | 3 custom decks |
| Rhythm Cards | 2 sheets | 80 | 2 custom decks |
| Judge Cards | 1 sheet | 12 | 1 custom deck |
| Stumble Cards | 1 sheet | 20 | 1 custom deck |

### Advanced: Save as TTS Object

Once you've created all the decks:

1. Arrange them on the table
2. Select all decks (drag select or Ctrl+A)
3. Right-click → **Save Object**
4. Name it "Beat by Beat - Complete Game"
5. Now you can spawn the entire game with one click!

### Tips for TTS

**Image Hosting:**
- Use direct image links (ending in `.png`)
- Make sure images are publicly accessible
- Imgur allows up to 1MB per image - our 2k sheets fit easily

**Testing:**
- Start with one small deck (judges or stumbles) to test your workflow
- Verify card order and orientation before importing all decks

**Card Quality:**
- 2048×2048 is good for online play
- For higher quality, edit `tts_generator.py` to use 4096×4096 (4k)
  - Change `SHEET_WIDTH = 4096` and `SHEET_HEIGHT = 4096`
  - Warning: Larger file sizes

**Card Order:**
- TTS reads cards left-to-right, top-to-bottom
- Cards are numbered 1-70 per sheet
- The generator outputs cards in CSV order

---

## 🔄 Complete Workflow

### Initial Setup

```bash
# 1. Generate cards
uv run python card-generator/generator.py

# 2. One-time: Install Playwright browser (for PDF generation)
uv run --with playwright playwright install chromium

# 3. Generate PDFs
uv run --with playwright python card-generator/pdf_generator.py

# 4. Generate TTS sprites
uv run --with Pillow python card-generator/tts_generator.py
```

### After Editing Card Data

```bash
# Regenerate everything at once
./generate-all.sh

# Or manually:
uv run python card-generator/generator.py
uv run --with playwright python card-generator/pdf_generator.py
uv run --with Pillow python card-generator/tts_generator.py
```

---

## 📂 Directory Structure

After running all generators:

```
beat-by-beat/
├── output/           # HTML files for browser printing
├── pdf/              # Print-ready PDFs
├── tts/              # Tabletop Simulator sprite sheets
└── card-data/        # Source CSV files
```

---

## 🎯 Use Cases

| Goal | Use This |
|------|----------|
| Quick preview in browser | `output/*.html` |
| Print at home | `pdf/*.pdf` |
| Send to print shop | `pdf/*.pdf` |
| Play online (TTS) | `tts/*.png` |
| Share for playtesting | `pdf/*.pdf` |

---

## 🐛 Troubleshooting

### PDF Generation

**Error: "playwright not found"**
```bash
# Install Playwright's browser
uv run --with playwright playwright install chromium
```

**PDFs are blank or missing colors**
- Check that `print_background=True` is in `pdf_generator.py`
- Verify HTML files exist in `output/` directory

### TTS Generation

**Error: "PIL not found"**
- Just use `--with Pillow` flag when running the script
- `uv` will install it automatically

**Cards look weird in TTS**
- Check image URLs are direct links (ending in `.png`)
- Verify images are publicly accessible
- Make sure Width=10, Height=7

**Text is too small**
- Increase font sizes in `tts_generator.py`
- Or use 4k resolution (4096×4096)

---

## 💡 Future Enhancements

- [ ] Automated TTS JSON deck configuration
- [ ] Direct upload to Imgur/Google Drive
- [ ] Higher resolution options (4k/8k)
- [ ] Custom card image integration
- [ ] Batch processing scripts
- [ ] TTS workshop upload tool

---

## 📝 Notes

**PDF Files:**
- PDFs use the same HTML/CSS as browser version
- Fully vector-based (scales perfectly)
- Embedded fonts and colors

**TTS Sprites:**
- Rasterized PNG images (bitmap)
- 2048×2048 = ~300-500KB per sheet
- Optimized for online play

**Quality:**
- PDFs are best for physical printing
- TTS sprites are optimized for screen viewing
- Both generated from same CSV source data
