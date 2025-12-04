#!/bin/bash
# One-time setup for Beat by Beat card generator

echo "🎭 Beat by Beat - Setup"
echo "======================"
echo ""

echo "Installing all dependencies..."
uv sync --all-extras

echo ""
echo "Installing Playwright browser..."
uv run playwright install chromium

echo ""
echo "✅ Setup complete!"
echo ""
echo "You can now generate cards:"
echo "  uv run python card-generator/generator.py      # HTML"
echo "  uv run python card-generator/pdf_generator.py  # PDF"
echo "  uv run python card-generator/tts_generator.py  # TTS"
echo "  ./generate-all.sh                               # Everything"
echo ""
