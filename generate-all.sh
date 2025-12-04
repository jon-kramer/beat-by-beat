#!/bin/bash
# Generate all card formats (HTML, PDF, TTS)

echo "🎭 Beat by Beat - Complete Card Generation"
echo "=========================================="
echo ""

# Step 1: Generate HTML cards
echo "Step 1/3: Generating HTML cards..."
uv run python card-generator/generator.py

echo ""

# Step 2: Generate PDFs
echo "Step 2/3: Generating PDFs..."
uv run python card-generator/pdf_generator.py

echo ""

# Step 3: Generate TTS sprites
echo "Step 3/3: Generating TTS sprite sheets..."
uv run python card-generator/tts_generator.py

echo ""
echo "✅ Generation complete!"
echo ""
echo "📂 Output locations:"
echo "  - HTML:  output/"
echo "  - PDF:   pdf/"
echo "  - TTS:   tts/"
echo ""
