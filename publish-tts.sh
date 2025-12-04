#!/bin/bash
# Publish TTS sprites to GitHub

set -e

echo "🎮 Beat by Beat - TTS Publisher"
echo "================================"
echo ""

# Step 1: Generate TTS sprites
echo "Step 1/4: Generating TTS sprite sheets..."
uv run python card-generator/tts_generator.py

echo ""

# Step 2: Check git status
echo "Step 2/4: Checking what changed..."
if ! git diff --quiet tts/ 2>/dev/null && ! git diff --cached --quiet tts/ 2>/dev/null; then
    echo ""
    echo "📝 Changes detected in tts/ folder:"
    git status tts/ --short
    echo ""
elif [ -n "$(git ls-files --others --exclude-standard tts/)" ]; then
    echo ""
    echo "📝 New files in tts/ folder:"
    git ls-files --others --exclude-standard tts/
    echo ""
else
    echo "✓ No changes detected in tts/ folder"
    echo ""
fi

# Step 3: Add to staging
echo "Step 3/4: Staging TTS files..."
git add tts/

# Step 4: Ask user if they want to commit
echo ""
read -p "Commit and push these changes? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Committing changes..."

    # Get commit message (or use default)
    read -p "Commit message (press enter for default): " commit_msg
    if [ -z "$commit_msg" ]; then
        commit_msg="Update TTS sprite sheets"
    fi

    git commit -m "$commit_msg"

    echo ""
    echo "Pushing to GitHub..."
    git push origin main

    echo ""
    echo "✅ Published to GitHub!"
    echo ""

    # Generate and display URLs
    ./get-tts-urls.sh
else
    echo ""
    echo "❌ Cancelled. Changes are staged but not committed."
    echo "   Run 'git reset HEAD tts/' to unstage"
    echo ""
fi
