#!/bin/bash
# Publish TTS sprites to GitHub

set -e

echo "🎮 Beat by Beat - TTS Publisher"
echo "================================"
echo ""

# Step 1: Generate TTS sprites
echo "Step 1/5: Generating TTS sprite sheets..."
uv run python card-generator/tts_generator.py

echo ""

# Step 2: Generate TTS JSON save file
echo "Step 2/5: Generating TTS save file..."
uv run python card-generator/tts_json_generator.py

echo ""

# Step 3: Check git status
echo "Step 3/5: Checking what changed..."
if ! git diff --quiet output/tts/ 2>/dev/null || ! git diff --cached --quiet output/tts/ 2>/dev/null || [ -n "$(git ls-files --others --exclude-standard output/tts/)" ]; then
    echo ""
    echo "📝 Changes detected in output/tts/ folder:"
    git status output/tts/ --short
    echo ""
    HAS_CHANGES=true
else
    echo "✓ No changes detected in output/tts/ folder"
    echo ""
    echo "Everything is already up to date! 🎉"
    echo ""
    echo "📋 To import in TTS:"
    echo "  Objects → Saved Objects → Import → output/tts/beat-by-beat.json"
    echo ""
    HAS_CHANGES=false
fi

# Step 4: If no changes, skip commit/push
if [ "$HAS_CHANGES" = false ]; then
    exit 0
fi

# Step 5: Commit and push changes
echo "Step 4/5: Staging TTS files..."
git add output/tts/

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
    echo "Step 5/5: Pushing to GitHub..."
    git push origin main

    echo ""
    echo "✅ Published to GitHub!"
    echo ""

    # Generate and display URLs
    $(dirname "$0")/get-tts-urls.sh
else
    echo ""
    echo "❌ Cancelled. Changes are staged but not committed."
    echo "   Run 'git reset HEAD output/tts/' to unstage"
    echo ""
fi
