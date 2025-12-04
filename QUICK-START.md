# Beat by Beat - Quick Start Guide

## 🎯 Print Your Cards in 3 Steps

### Step 1: Open the Card Browser
Open `output/index.html` in your web browser

### Step 2: Select & Print
Click on any card type to open it, then print:
- **Move Cards** → 19 sheets (all in one file)
- **Rhythm Cards** → 9 sheets (all in one file)
- **Judge Cards** → 2 sheets (all in one file)
- **Stumble Cards** → 3 sheets (all in one file)

### Step 3: Print Settings
```
Paper:       Letter (8.5" × 11")
Margins:     None / Minimum
Scale:       100%
Backgrounds: ON ⚠️ REQUIRED
```

## 📋 What Gets Printed

Each HTML file contains **multiple sheets** that print automatically:

| File | Contains | What Prints |
|------|----------|-------------|
| `move-cards.html` | 170 cards | 19 sheets automatically |
| `rhythm-cards.html` | 80 cards | 9 sheets automatically |
| `judge-cards.html` | 12 cards | 2 sheets automatically |
| `stumble-cards.html` | 20 cards | 3 sheets automatically |

**Total: 33 sheets, 282 cards**

## 🔄 Double-Sided Printing

### Option 1: Automatic Duplex
If your printer supports it:
1. Enable duplex/2-sided in print settings
2. Print the fronts file
3. Done!

### Option 2: Manual Duplex
1. Print all fronts first (e.g., `move-cards.html` = 19 sheets)
2. Take the stack, flip it over
3. Print backs file (e.g., `move-backs.html`)
4. Repeat back sheet 19 times (or use duplex setting to duplicate)

**Pro tip:** Do a test print with 1 sheet first to check flip orientation!

## 📐 Each Sheet Contains

3×3 grid = **9 cards per sheet**

Card size: 2.5" × 3.5" (standard poker size)

## ✂️ After Printing

1. **Cut** along card borders (use ruler + craft knife, or paper trimmer)
2. **Sleeve** with standard poker sleeves (optional but recommended)
3. **Play!**

## 🎨 Card Colors

Each style has its own color:
- **Latin** = Coral
- **Ballroom** = Deep Indigo
- **Classical** = Soft Sage
- **Jazz** = Warm Gold
- **Street** = Slate Blue
- **Styleless** = Cream

Multi-style cards have gradient backgrounds!

## ❓ Troubleshooting

**Colors don't print?**
→ Enable "Background Graphics" in print settings

**Wrong size?**
→ Set scale to 100%, disable "fit to page"

**Backs don't align?**
→ Test print 1 sheet to check flip direction

## 🔄 Regenerate Cards

If you edit the CSV files:
```bash
./generate.sh
```

Or manually:
```bash
python3 card-generator/generator.py
```

## 📚 More Info

- **README.md** - Technical details
- **PRINTING-GUIDE.md** - Complete printing instructions
- **docs/** - Game rules and documentation
