#!/bin/bash
# Generate GitHub raw URLs for TTS sprite sheets

echo "📋 TTS Image URLs for Tabletop Simulator"
echo "========================================="
echo ""

# Get the GitHub repo info
REMOTE_URL=$(git config --get remote.origin.url)

if [ -z "$REMOTE_URL" ]; then
    echo "❌ Error: No git remote found"
    echo "   Run this after pushing to GitHub"
    exit 1
fi

# Extract username/repo from various GitHub URL formats
if [[ $REMOTE_URL =~ github.com[:/]([^/]+)/([^/.]+) ]]; then
    USERNAME="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
else
    echo "❌ Error: Could not parse GitHub URL: $REMOTE_URL"
    exit 1
fi

BRANCH="main"
BASE_URL="https://raw.githubusercontent.com/${USERNAME}/${REPO}/${BRANCH}/tts"

echo "Repository: ${USERNAME}/${REPO}"
echo "Branch: ${BRANCH}"
echo ""

# Find all PNG files in tts/ directory
if [ ! -d "tts" ]; then
    echo "❌ Error: tts/ directory not found"
    echo "   Run './publish-tts.sh' first"
    exit 1
fi

PNG_FILES=$(find tts -name "*.png" -type f | sort)

if [ -z "$PNG_FILES" ]; then
    echo "❌ Error: No PNG files found in tts/"
    echo "   Run './publish-tts.sh' first"
    exit 1
fi

echo "🎴 Card Deck URLs:"
echo "=================="
echo ""

# Categorize and display URLs
echo "Move Cards:"
echo "$PNG_FILES" | grep "move-cards" | while read -r file; do
    filename=$(basename "$file")
    echo "  ${BASE_URL}/${filename}"
done
echo ""

echo "Move Card Backs:"
echo "$PNG_FILES" | grep "move-backs" | while read -r file; do
    filename=$(basename "$file")
    echo "  ${BASE_URL}/${filename}"
done
echo ""

echo "Rhythm Cards:"
echo "$PNG_FILES" | grep "rhythm-cards" | while read -r file; do
    filename=$(basename "$file")
    echo "  ${BASE_URL}/${filename}"
done
echo ""

echo "Rhythm Card Backs:"
echo "$PNG_FILES" | grep "rhythm-backs" | while read -r file; do
    filename=$(basename "$file")
    echo "  ${BASE_URL}/${filename}"
done
echo ""

echo "Judge Cards:"
echo "$PNG_FILES" | grep "judge-cards" | while read -r file; do
    filename=$(basename "$file")
    echo "  ${BASE_URL}/${filename}"
done
echo ""

echo "Judge Card Backs:"
echo "$PNG_FILES" | grep "judge-backs" | while read -r file; do
    filename=$(basename "$file")
    echo "  ${BASE_URL}/${filename}"
done
echo ""

echo "Stumble Cards:"
echo "$PNG_FILES" | grep "stumble-cards" | while read -r file; do
    filename=$(basename "$file")
    echo "  ${BASE_URL}/${filename}"
done
echo ""

echo "Stumble Card Backs:"
echo "$PNG_FILES" | grep "stumble-backs" | while read -r file; do
    filename=$(basename "$file")
    echo "  ${BASE_URL}/${filename}"
done
echo ""

echo "💡 Usage in Tabletop Simulator:"
echo "================================"
echo "1. Objects → Components → Custom → Deck"
echo "2. Paste Front URL and Back URL"
echo "3. Set Width: 10, Height: 7"
echo "4. Set Number: 70 (or less for partial sheets)"
echo "5. Click Import"
echo ""
