# Tabletop Simulator - GitHub Hosting Guide

Host your TTS sprite sheets on GitHub for free, permanent URLs.

## Quick Start

### First Time Only

```bash
# 1. Set up GitHub (see docs/GITHUB-SETUP.md for details)
gh auth login
gh repo create beat-by-beat --public --source=. --remote=origin
git add .
git commit -m "Initial commit"
git push -u origin main

# 2. Publish TTS sprites
./scripts/publish-tts.sh
```

### Every Time You Update Cards

```bash
# Edit your cards
vim card-data/moves.csv

# Regenerate and publish
./scripts/publish-tts.sh
```

The script will:
1. Generate TTS sprites
2. Show what changed
3. Ask "Commit and push? (y/n)"
4. If yes: commit, push, generate TTS save file, and show URLs
5. Import the JSON file into TTS

## Using in Tabletop Simulator

### Option 1: One-Click Import (Recommended)

1. In TTS: **Objects** → **Saved Objects** → **Import**
2. Select `output/tts/beat-by-beat.json`
3. All decks spawn on the table automatically!

This is the easiest method - all decks are pre-configured with proper URLs and card counts.

### Option 2: Manual Import (Legacy Method)

If you need to create custom decks manually:

#### Import a Custom Deck

1. In TTS: **Objects** → **Components** → **Custom** → **Deck**
2. Fill in the form:

| Field | Value | Example |
|-------|-------|---------|
| **Face** | GitHub raw URL to front sprite | `https://raw.githubusercontent.com/USERNAME/beat-by-beat/main/tts/move-cards_1.png` |
| **Back** | GitHub raw URL to back sprite | `https://raw.githubusercontent.com/USERNAME/beat-by-beat/main/tts/move-backs.png` |
| **Width** | `10` | (TTS uses 10×7 grids) |
| **Height** | `7` | (70 cards per sheet) |
| **Number** | Cards in this sheet | `70` for full, less for partial |
| **Unique Backs** | No | (all backs are identical) |

3. Click **Import**

### Example: Move Cards

You have 170 move cards = 3 sprite sheets:

**Deck 1:**
- Face: `.../move-cards_1.png`
- Back: `.../move-backs.png`
- Number: 70

**Deck 2:**
- Face: `.../move-cards_2.png`
- Back: `.../move-backs.png`
- Number: 70

**Deck 3:**
- Face: `.../move-cards_3.png`
- Back: `.../move-backs.png`
- Number: 30

Repeat for rhythm, judge, and stumble cards.

## Getting URLs

The `./scripts/publish-tts.sh` script automatically prints all URLs after pushing.

**Or get them anytime:**

```bash
./scripts/get-tts-urls.sh
```

This shows organized URLs ready to copy/paste.

## Workflow Example

```bash
# Make changes to cards
vim card-data/moves.csv

# Regenerate everything
./scripts/generate-all.sh

# Test locally in browser
open output/html/index.html

# When ready, publish to GitHub
./scripts/publish-tts.sh

# Output:
# 🎮 Beat by Beat - TTS Publisher
# Step 1/4: Generating TTS sprite sheets...
# Generated: move-cards_1.png
# ...
# Step 2/4: Checking what changed...
# M tts/move-cards_1.png
#
# Step 3/4: Staging TTS files...
#
# Commit and push these changes? (y/n) y
#
# Commit message (press enter for default): Add new Latin moves
# Committing changes...
# Pushing to GitHub...
# ✅ Published to GitHub!
#
# 📋 TTS Image URLs for Tabletop Simulator
# =========================================
# Move Cards:
#   https://raw.githubusercontent.com/.../move-cards_1.png
#   https://raw.githubusercontent.com/.../move-cards_2.png
#   ...
```

Copy the URLs and paste into TTS!

## Advantages Over Imgur

| Feature | GitHub | Imgur |
|---------|--------|-------|
| **Permanence** | Forever (as long as repo exists) | May expire after inactivity |
| **Version control** | Full git history | No versioning |
| **Automation** | Script handles everything | Manual upload |
| **Cost** | Free (public repo) | Free |
| **Privacy** | Public repo required | Anonymous upload |
| **Reliability** | Very high (GitHub CDN) | Very high |

## Tips

### Organize Your Decks

Save your TTS deck configurations:

1. After importing all decks, arrange them on the table
2. Select all decks (drag-select)
3. Right-click → **Save Object**
4. Name: "Beat by Beat - Complete Set"
5. Next time: **Objects** → **Saved Objects** → spawn instantly!

### Update Workflow

When you change cards:

1. `./scripts/publish-tts.sh` (generates + pushes to GitHub)
2. In TTS, **reload** the affected decks:
   - Delete old deck
   - Re-import with same URL
   - GitHub serves the updated image!

### Sharing with Players

Share your GitHub raw URLs with players:
- They can import the same decks
- Everyone sees the same cards
- Perfect for online playtesting

## Troubleshooting

### "remote: Repository not found"

Create the GitHub repo first:
```bash
gh repo create beat-by-beat --public --source=. --remote=origin
```

### URLs show 404 in TTS

- Repo must be **public**
- Wait 1-2 minutes after pushing (CDN cache)
- Check URL is exact (case-sensitive)

### "failed to push"

```bash
git pull origin main --rebase
git push origin main
```

### Want to see what's on GitHub?

```bash
# View in browser
gh repo view --web

# Or visit manually
# https://github.com/USERNAME/beat-by-beat
```

## Alternative: Private Repo with Git LFS

For private hosting (requires Git LFS setup):

1. Create private repo
2. Set up Git LFS
3. Use GitHub's authenticated URLs (more complex)
4. Or use Imgur for easier private testing

For public playtesting, public repo is simpler and free!

## Summary

**Setup once:**
- docs/GITHUB-SETUP.md has full instructions
- Takes ~5 minutes

**Use forever:**
- `./scripts/publish-tts.sh` → copies URLs → paste in TTS
- That's it!
