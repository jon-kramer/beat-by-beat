#!/usr/bin/env python3
"""
Tabletop Simulator Generator for Beat by Beat Cards (v2)
Renders HTML cards directly into TTS sprite sheet layout
This ensures perfect consistency between HTML/PDF and TTS formats
"""

import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright


# TTS requirements:
# - 10 cards wide × 7 cards tall = 70 cards per sheet
# - Resolution: 4096×4096 pixels for high quality (TTS recommended)
# - Can also use 2048×2048 for smaller file sizes
SHEET_WIDTH = 4096
SHEET_HEIGHT = 4096
CARDS_PER_ROW = 10
CARDS_PER_COL = 7
CARDS_PER_SHEET = 70


def create_tts_html(card_htmls, css_content):
    """Create HTML with cards in a 10x7 grid for TTS sprite sheet"""
    # Cards keep their natural size (2.5in × 3.5in)
    # We'll render at a large viewport and scale during screenshot

    cards_html = '\n'.join(card_htmls)

    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            margin: 0;
            padding: 0;
            background: white;
        }}

        .tts-grid {{
            display: grid;
            grid-template-columns: repeat({CARDS_PER_ROW}, 2.5in);
            grid-template-rows: repeat({CARDS_PER_COL}, 3.5in);
            gap: 0;
        }}

        .card {{
            width: 2.5in !important;
            height: 3.5in !important;
            margin: 0 !important;
        }}

        /* Import original card styles */
        {css_content}
    </style>
</head>
<body>
    <div class="tts-grid">
        {cards_html}
    </div>
</body>
</html>'''
    return html


async def extract_cards_from_html(html_path):
    """Extract card HTML elements and CSS from an HTML file"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f'file://{html_path.absolute()}')

        # Extract CSS
        css_content = await page.evaluate('''() => {
            const styleSheets = Array.from(document.styleSheets);
            return styleSheets.map(sheet => {
                try {
                    return Array.from(sheet.cssRules).map(rule => rule.cssText).join('\\n');
                } catch (e) {
                    return '';
                }
            }).join('\\n');
        }''')

        # Get all card elements (excluding backs)
        card_elements = await page.query_selector_all('.card:not(.card-back)')
        card_htmls = []
        for card in card_elements:
            html = await card.evaluate('(el) => el.outerHTML')
            card_htmls.append(html)

        await browser.close()

        return card_htmls, css_content


async def extract_card_back_from_html(html_path):
    """Extract card back HTML and CSS from an HTML file"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f'file://{html_path.absolute()}')

        # Extract CSS
        css_content = await page.evaluate('''() => {
            const styleSheets = Array.from(document.styleSheets);
            return styleSheets.map(sheet => {
                try {
                    return Array.from(sheet.cssRules).map(rule => rule.cssText).join('\\n');
                } catch (e) {
                    return '';
                }
            }).join('\\n');
        }''')

        # Get the card back element
        card_back = await page.query_selector('.card-back')
        if card_back:
            back_html = await card_back.evaluate('(el) => el.outerHTML')
        else:
            back_html = None

        await browser.close()

        return back_html, css_content


async def render_sprite_sheet(card_htmls, css_content, output_path):
    """Render cards as TTS sprite sheets"""
    # Split into sheets of 70 cards
    num_sheets = (len(card_htmls) + CARDS_PER_SHEET - 1) // CARDS_PER_SHEET

    # Natural grid size at 96 DPI: 10 × 2.5in = 25in, 7 × 3.5in = 24.5in
    # At 96 DPI: 2400px × 2352px
    # We want 4096px output, so scale factor is 4096/2400 ≈ 1.7
    natural_width = int(10 * 2.5 * 96)  # 2400px
    natural_height = int(7 * 3.5 * 96)  # 2352px

    # Calculate device scale factor to get target resolution
    scale_factor = SHEET_WIDTH / natural_width

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={'width': natural_width, 'height': natural_height},
            device_scale_factor=scale_factor
        )
        page = await context.new_page()

        for sheet_num in range(num_sheets):
            start_idx = sheet_num * CARDS_PER_SHEET
            end_idx = min(start_idx + CARDS_PER_SHEET, len(card_htmls))
            sheet_cards = card_htmls[start_idx:end_idx]

            # Pad with empty divs if needed
            while len(sheet_cards) < CARDS_PER_SHEET:
                sheet_cards.append('<div class="card" style="background: white;"></div>')

            # Create HTML for this sheet
            html = create_tts_html(sheet_cards, css_content)

            # Render
            await page.set_content(html)
            await page.wait_for_load_state('networkidle')

            # Screenshot
            if num_sheets > 1:
                filename = f'{output_path.stem}_{sheet_num + 1}.png'
            else:
                filename = f'{output_path.stem}.png'

            save_path = output_path.parent / filename
            await page.screenshot(path=str(save_path), full_page=True)
            print(f'Generated: {filename}')

        await browser.close()


async def render_card_backs(html_path, output_path):
    """Render card back sprite sheet"""
    back_html, css_content = await extract_card_back_from_html(html_path)

    if not back_html:
        print(f'Warning: No card back found in {html_path.name}')
        return

    # Create sheet filled with card backs
    back_htmls = [back_html] * CARDS_PER_SHEET

    # Use same scaling approach as fronts
    natural_width = int(10 * 2.5 * 96)
    natural_height = int(7 * 3.5 * 96)
    scale_factor = SHEET_WIDTH / natural_width

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={'width': natural_width, 'height': natural_height},
            device_scale_factor=scale_factor
        )
        page = await context.new_page()

        html = create_tts_html(back_htmls, css_content)

        await page.set_content(html)
        await page.wait_for_load_state('networkidle')

        await page.screenshot(path=str(output_path), full_page=True)
        print(f'Generated: {output_path.name}')

        await browser.close()


async def main():
    """Generate TTS sprite sheets from HTML cards"""
    base_dir = Path(__file__).parent.parent
    output_dir = base_dir / 'output' / 'html'
    tts_dir = base_dir / 'output' / 'tts'

    # Create TTS directory
    tts_dir.mkdir(parents=True, exist_ok=True)

    print('🎭 Beat by Beat - TTS Generator v2 (HTML-based)')
    print('=' * 50)
    print()

    # Check if HTML files exist
    if not output_dir.exists():
        print('❌ Error: output/html/ directory not found')
        print('   Run ./scripts/generate-all.sh or python card-generator/generator.py first')
        return

    # Generate move cards
    move_html = output_dir / 'move-cards.html'
    if move_html.exists():
        print('Generating move card sprites...')
        card_htmls, css = await extract_cards_from_html(move_html)
        print(f'  Found {len(card_htmls)} move cards')
        await render_sprite_sheet(card_htmls, css, tts_dir / 'move-cards')

        print('Generating move card backs...')
        move_backs_html = output_dir / 'move-backs.html'
        await render_card_backs(move_backs_html, tts_dir / 'move-backs.png')

    # Generate rhythm cards
    rhythm_html = output_dir / 'rhythm-cards.html'
    if rhythm_html.exists():
        print('\nGenerating rhythm card sprites...')
        card_htmls, css = await extract_cards_from_html(rhythm_html)
        print(f'  Found {len(card_htmls)} rhythm cards')
        await render_sprite_sheet(card_htmls, css, tts_dir / 'rhythm-cards')

        print('Generating rhythm card backs...')
        rhythm_backs_html = output_dir / 'rhythm-backs.html'
        await render_card_backs(rhythm_backs_html, tts_dir / 'rhythm-backs.png')

    # Generate judge cards
    judge_html = output_dir / 'judge-cards.html'
    if judge_html.exists():
        print('\nGenerating judge card sprites...')
        card_htmls, css = await extract_cards_from_html(judge_html)
        print(f'  Found {len(card_htmls)} judge cards')
        await render_sprite_sheet(card_htmls, css, tts_dir / 'judge-cards')

        print('Generating judge card backs...')
        judge_backs_html = output_dir / 'judge-backs.html'
        await render_card_backs(judge_backs_html, tts_dir / 'judge-backs.png')

    # Generate stumble cards
    stumble_html = output_dir / 'stumble-cards.html'
    if stumble_html.exists():
        print('\nGenerating stumble card sprites...')
        card_htmls, css = await extract_cards_from_html(stumble_html)
        print(f'  Found {len(card_htmls)} stumble cards')
        await render_sprite_sheet(card_htmls, css, tts_dir / 'stumble-cards')

        print('Generating stumble card backs...')
        stumble_backs_html = output_dir / 'stumble-backs.html'
        await render_card_backs(stumble_backs_html, tts_dir / 'stumble-backs.png')

    print()
    print(f'✅ TTS sprite sheets generated in: {tts_dir}')
    print()
    print('Cards now match HTML/PDF rendering exactly!')
    print()


if __name__ == '__main__':
    asyncio.run(main())
