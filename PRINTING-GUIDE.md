# Beat by Beat - Printing Guide

## Quick Start

1. Open `output/index.html` in your web browser
2. Click on any sheet to preview it
3. Print using your browser's print function

## What You'll Print

### Complete Game Set (for 5 players)

| Component | Sheets | Cards |
|-----------|--------|-------|
| Move Cards | 19 | 170 |
| Rhythm Cards | 9 | 80 |
| Judge Cards | 2 | 12 |
| Stumble Cards | 3 | 20 |
| **Fronts Total** | **33** | **282** |
| Card Backs | 4 | - |
| **Grand Total** | **37** | **282** |

## Print Settings

**Critical settings for correct output:**

- **Paper Size**: Letter (8.5" × 11")
- **Margins**: None / Minimum
- **Scale**: 100% (no fit-to-page)
- **Background Graphics**: **ON** (required for colors)
- **Print Quality**: Best/High

## Printing Double-Sided Cards

### Method 1: Manual Duplex
1. Print all front sheets first
2. Take printed sheets, flip entire stack
3. Feed back into printer (test orientation first!)
4. Print corresponding back sheets

### Method 2: Single-Sided
1. Print fronts on one color paper
2. Print backs on different color paper
3. Glue or sleeve together

### Tips
- Do a **test print** with one sheet first
- Mark the top-left corner to check flip orientation
- Card backs are identical for each type, so you can print the same back sheet multiple times

## Cutting Guide

Each sheet has a 3×3 grid of cards (9 cards per sheet).

**Card dimensions**: 2.5" × 3.5" (standard poker size)

### Cutting Tools

**Option 1: Ruler + Craft Knife**
- Use a metal ruler and cutting mat
- Cut carefully along card borders

**Option 2: Paper Trimmer**
- Guillotine-style trimmer works well
- Cut one direction, then the other

**Option 3: Professional**
- Local print shop can cut for you
- Provide dimensions: 2.5" × 3.5" cards in 3×3 grid

### Cutting Marks
The generator adds 2px borders to help align cuts. Cut along the outer edge of these borders.

## Card Protection

### Sleeves
Standard poker-size sleeves (2.5" × 3.5" / 63.5mm × 88mm) fit perfectly.

Recommended brands:
- Ultra Pro
- Dragon Shield
- Fantasy Flight Games

**Sleeve count needed**: 282+ sleeves (buy 300 to be safe)

### Lamination
Not recommended - makes cards too thick and slippery to shuffle well.

## Paper Recommendations

### Budget Option
- **Type**: Standard cardstock (65-110 lb / 176-300 gsm)
- **Weight**: 80-110 lb is ideal
- **Finish**: Matte (less glare)

### Premium Option
- **Type**: Linen cardstock
- **Weight**: 100-110 lb
- **Finish**: Matte or linen texture
- **Benefit**: Better feel, more durable

### Where to Buy
- Local office supply stores (Staples, Office Depot)
- Online: Amazon, Paper Source
- Print shops often have better quality cardstock

## Cost Estimate

### At-Home Printing (Budget)
- Cardstock: $15-25
- Ink/toner: $10-30
- Card sleeves: $15-25
- **Total**: ~$40-80

### Print Shop (Premium)
- Printing on premium cardstock: $40-80
- Professional cutting: $20-40
- Card sleeves: $15-25
- **Total**: ~$75-145

## Regenerating Cards

If you edit the CSV data files and want to regenerate:

```bash
./generate.sh
```

Or manually:

```bash
python3 card-generator/generator.py
```

## Adding Custom Artwork

The system supports custom artwork for each card:

1. Create SVG or PNG files for each card
2. Name them according to the `image_file` column in CSVs
3. Place in `images/` directory
4. Re-run generator

Current version uses **placeholder graphics** (type icons on colored backgrounds).

## Troubleshooting

### Cards Are Wrong Size
- Check print scale is 100%
- Disable "fit to page" or "shrink to fit"
- Check margins are set to minimum/none

### Colors Don't Print
- Enable "Background Graphics" in print settings
- Some browsers call this "Print backgrounds"

### Gradients Look Banded
- Increase print quality setting
- Use "Best" or "High Quality" mode

### Text Is Too Small
- This is expected - cards are small
- Consider using larger font sizes in generator.py if needed
- Premium printing usually has better text clarity

### Alignment Issues on Back
- Do a test print first
- Mark top-left corner to understand flip orientation
- Your printer may have specific duplex quirks

## Questions?

Refer to:
- `README.md` - Technical documentation
- `docs/` - Game rules and card details
- `card-data/` - CSV files with all card data

## License & Attribution

Game design and mechanics are original to Beat by Beat.
Card generation system is provided as-is for personal/playtesting use.
