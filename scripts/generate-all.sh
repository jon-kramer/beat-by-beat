#!/bin/bash
# Generate all card formats (HTML, PDF, TTS)

set -e  # Exit on error

echo "🎭 Beat by Beat - Complete Card Generation"
echo "=========================================="
echo ""

# Step 1: Generate HTML cards
echo "Step 1/4: Generating HTML cards..."
uv run python card-generator/generator.py

echo ""

# Step 2: Generate PDFs
echo "Step 2/4: Generating PDFs..."
if ! uv run python card-generator/pdf_generator.py 2>&1; then
    echo ""
    echo "❌ PDF generation failed!"
    echo ""
    echo "💡 This usually means dependencies aren't installed."
    echo "   Run one of these commands:"
    echo ""
    echo "   ./setup.sh                    # Install everything"
    echo "   uv sync --all-extras          # Or just sync dependencies"
    echo ""
    exit 1
fi

echo ""

# Step 3: Generate TTS sprites
echo "Step 3/4: Generating TTS sprite sheets..."
if ! uv run python card-generator/tts_generator.py 2>&1; then
    echo ""
    echo "❌ TTS generation failed!"
    echo ""
    echo "💡 This usually means dependencies aren't installed."
    echo "   Run one of these commands:"
    echo ""
    echo "   ./setup.sh                    # Install everything"
    echo "   uv sync --all-extras          # Or just sync dependencies"
    echo ""
    exit 1
fi

echo ""

# Step 4: Generate TTS JSON save file
echo "Step 4/4: Generating TTS JSON save file..."
if ! uv run python card-generator/tts_json_generator.py 2>&1; then
    echo ""
    echo "❌ TTS JSON generation failed!"
    echo ""
    echo "💡 This usually means dependencies aren't installed or git remote isn't set."
    echo "   Run one of these commands:"
    echo ""
    echo "   ./setup.sh                    # Install everything"
    echo "   uv sync --all-extras          # Or just sync dependencies"
    echo ""
    exit 1
fi

echo ""
echo "✅ Generation complete!"
echo ""
echo "📂 Output locations:"
echo "  - HTML:      output/html/"
echo "  - PDF:       output/pdf/"
echo "  - TTS:       output/tts/"
echo "  - TTS JSON:  output/tts/beat-by-beat.json"
echo ""
