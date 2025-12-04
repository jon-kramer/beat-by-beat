# Beat by Beat - Command Reference

Quick reference for all generation commands.

## 📋 Basic Commands

### Generate HTML Cards
```bash
uv run python card-generator/generator.py
```
**Output:** `output/*.html` (4 files)
**Use for:** Browser printing, quick preview

### Generate All Formats
```bash
./generate-all.sh
```
**Output:** HTML + PDF + TTS
**Use for:** Complete regeneration after editing CSVs

## 📄 PDF Generation

### One-Time Setup
```bash
# Install Playwright's Chromium browser
uv run --with playwright playwright install chromium
```
**Required:** First time only (~100MB download)

### Generate PDFs
```bash
uv run --with playwright python card-generator/pdf_generator.py
```
**Output:** `pdf/*.pdf` (8 files)
**Use for:** Print shops, physical printing

## 🎮 Tabletop Simulator

### Generate TTS Sprites
```bash
uv run --with Pillow python card-generator/tts_generator.py
```
**Output:** `tts/*.png` (sprite sheets)
**Use for:** Online play in Tabletop Simulator

**Note:** The `--with` flags tell `uv` to install packages on-demand

## 📦 Output Summary

| Command | Format | Location | Files | Use Case |
|---------|--------|----------|-------|----------|
| `generator.py` | HTML | `output/` | 9 files | Browser preview/print |
| `pdf_generator.py` | PDF | `pdf/` | 8 files | Professional printing |
| `tts_generator.py` | PNG | `tts/` | ~8 files | Online play (TTS) |
| `generate-all.sh` | All | All dirs | ~25 files | Everything at once |

## 🔄 Typical Workflows

### First Time Setup
```bash
# 1. Generate initial cards
uv run python card-generator/generator.py

# 2. Preview in browser
open output/index.html

# 3. (Optional) Install Playwright browser for PDF generation
uv run --with playwright playwright install chromium
```

### After Editing CSV Data
```bash
# Regenerate everything
./generate-all.sh

# Or regenerate specific formats:
uv run python card-generator/generator.py                         # HTML only
uv run --with playwright python card-generator/pdf_generator.py   # PDF only
uv run --with Pillow python card-generator/tts_generator.py       # TTS only
```

### Preparing for Print Shop
```bash
# Generate PDFs
uv run --with playwright python card-generator/pdf_generator.py

# PDFs are in pdf/ directory
# Send these to print shop
```

### Setting Up TTS Game
```bash
# 1. Generate sprites
uv run --with Pillow python card-generator/tts_generator.py

# 2. Upload PNGs from tts/ to Imgur

# 3. Import in TTS using image URLs
```

## 🛠️ Troubleshooting Commands

### Check if PDF tools are installed
```bash
uv run python -c "import playwright; print('✓ Playwright installed')"
```

### Check if TTS tools are installed
```bash
uv run python -c "import PIL; print('✓ Pillow installed')"
```

### Install Playwright browser (for PDFs)
```bash
uv run --with playwright playwright install chromium
```

**Note:** Python packages are installed automatically via `--with` flags

### Clean and regenerate everything
```bash
# Remove old outputs
rm -rf output/*.html pdf/*.pdf tts/*.png

# Regenerate all
./generate-all.sh
```

## 📊 File Counts

After running all generators:

```
output/    9 files  (HTML + index)
pdf/       8 files  (PDFs for printing)
tts/      ~8 files  (PNG sprite sheets)
```

Total: ~25 generated files from 4 CSV source files

## 🎯 Quick Reference

| I want to... | Command |
|--------------|---------|
| Preview cards | `open output/index.html` |
| Print at home | Open PDFs in `pdf/` |
| Play on TTS | Upload `tts/*.png` to Imgur |
| Update cards | Edit CSVs, then `./generate-all.sh` |
| Share for playtesting | Share `pdf/` folder |
| Make just one card type | Edit CSVs, run `generator.py` |

## 💡 Pro Tips

**Batch Processing:**
- Use `generate-all.sh` after any CSV changes
- Scripts are idempotent (safe to run multiple times)

**Version Control:**
- Commit CSV files (source data)
- Add output/pdf/tts to `.gitignore` (generated files)

**Automation:**
- Add `./generate-all.sh` to your build process
- Use cron/scheduled tasks for nightly builds

**Performance:**
- HTML generation: <1 second
- PDF generation: ~5-10 seconds
- TTS generation: ~10-15 seconds
- Total: ~30 seconds for everything
