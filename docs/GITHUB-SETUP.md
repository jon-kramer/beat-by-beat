# GitHub Setup for TTS Hosting

This guide helps you host your TTS sprite sheets on GitHub for free, permanent hosting.

## Step 1: Install GitHub CLI (if needed)

If `gh` command doesn't work, install it:

```bash
# macOS
brew install gh

# Or download from: https://cli.github.com/
```

## Step 2: Authenticate with GitHub

```bash
gh auth login
```

Follow the prompts to authenticate.

## Step 3: Create GitHub Repository

From this directory, run:

```bash
gh repo create beat-by-beat --public --source=. --remote=origin
```

This creates a public repo named `beat-by-beat` and sets it as your remote.

**Or manually:**
1. Go to https://github.com/new
2. Name: `beat-by-beat`
3. Public (free hosting requires public repo)
4. Don't initialize with README (we already have files)
5. Create repository
6. Copy the repo URL
7. Run: `git remote add origin <URL>`

## Step 4: Initial Commit

```bash
# Add all files
git add .

# Commit
git commit -m "Initial commit: Beat by Beat card generator"

# Push to GitHub
git push -u origin main
```

## Step 5: Publish TTS Sprites

Now you can use the automated workflow:

```bash
./scripts/publish-tts.sh
```

This will:
1. Generate TTS sprite sheets
2. Show you what changed
3. Ask if you want to commit & push
4. Push to GitHub
5. Show you the URLs to use in TTS

## Step 6: Get URLs Anytime

To see the TTS URLs without regenerating:

```bash
./scripts/get-tts-urls.sh
```

## How It Works

### GitHub Raw URLs

GitHub serves files via raw URLs:
```
https://raw.githubusercontent.com/USERNAME/REPO/main/tts/move-cards_1.png
```

These URLs:
- Are permanent (as long as repo exists)
- Work in Tabletop Simulator
- Are free (for public repos)
- Update automatically when you push changes

### Workflow

```bash
# Edit your CSV files
vim card-data/moves.csv

# Regenerate and publish to GitHub
./scripts/publish-tts.sh

# Copy the URLs it prints
# Paste into Tabletop Simulator
```

## Using Git LFS (Optional but Recommended)

For better handling of large PNG files, use Git LFS:

```bash
# Install Git LFS
brew install git-lfs  # macOS
# or download from: https://git-lfs.github.com/

# Initialize in your repo
git lfs install

# Already configured in .gitattributes!
# Just commit and push normally
```

Git LFS stores large files more efficiently.

## Troubleshooting

### "gh: command not found"

Install GitHub CLI: https://cli.github.com/

### "failed to push some refs"

```bash
# Pull first
git pull origin main --rebase

# Then push
git push origin main
```

### URLs don't work in TTS

- Make sure repo is **public** (private repos don't work with raw URLs)
- Wait a minute after pushing (GitHub CDN needs to update)
- Check URLs are exact (case-sensitive)

### Want to use a different branch?

Edit `scripts/get-tts-urls.sh` and change:
```bash
BRANCH="main"
```
to:
```bash
BRANCH="your-branch-name"
```

## Privacy Note

Since the repo must be public for free hosting:
- Your card designs will be visible to anyone
- This is fine for playtesting and sharing with players
- If you want private hosting, use Imgur or paid GitHub LFS

## Summary

**One-time setup:**
```bash
gh auth login
gh repo create beat-by-beat --public --source=. --remote=origin
git add .
git commit -m "Initial commit"
git push -u origin main
```

**Every time you update cards:**
```bash
./scripts/publish-tts.sh
```

That's it! The script handles the rest.
