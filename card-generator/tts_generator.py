#!/usr/bin/env python3
"""
Tabletop Simulator Generator for Beat by Beat Cards
Creates sprite sheets compatible with TTS custom decks
"""

import csv
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


# TTS requirements:
# - 10 cards wide × 7 cards tall = 70 cards per sheet
# - Recommended resolution: 4096×4096 pixels (or 2048×2048 for smaller files)
# - Each card: 409.6 × 585.14 pixels at 4k (or 204.8 × 292.57 at 2k)

# We'll use 2k for faster generation
SHEET_WIDTH = 2048
SHEET_HEIGHT = 2048
CARDS_PER_ROW = 10
CARDS_PER_COL = 7
CARDS_PER_SHEET = 70

CARD_WIDTH = SHEET_WIDTH // CARDS_PER_ROW  # 204.8
CARD_HEIGHT = SHEET_HEIGHT // CARDS_PER_COL  # 292.57


# Color scheme (same as HTML generator)
COLORS = {
    'Latin': '#FF6B6B',
    'Ballroom': '#6B5B95',
    'Classical': '#8FB996',
    'Jazz': '#E9C46A',
    'Street': '#457B9D',
    'Styleless': '#FAF8F3',
}


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def get_style_color(style):
    """Get RGB color for a style"""
    if not style:
        return hex_to_rgb(COLORS['Styleless'])

    styles = [s.strip() for s in style.split('/')]
    if len(styles) == 1:
        return hex_to_rgb(COLORS.get(styles[0], COLORS['Styleless']))
    else:
        # For multi-style, blend the two colors
        color1 = hex_to_rgb(COLORS.get(styles[0], COLORS['Styleless']))
        color2 = hex_to_rgb(COLORS.get(styles[1], COLORS['Styleless']))
        return tuple((c1 + c2) // 2 for c1, c2 in zip(color1, color2))


def create_move_card(draw, x, y, move, font_large, font_medium, font_small):
    """Draw a move card on the sprite sheet"""
    # Card background
    draw.rectangle([x, y, x + CARD_WIDTH, y + CARD_HEIGHT], fill='white', outline='black', width=2)

    # Header with style color
    header_height = 40
    style_color = get_style_color(move['style'])
    draw.rectangle([x, y, x + CARD_WIDTH, y + header_height], fill=style_color)

    # Card name
    name = move['name']
    draw.text((x + CARD_WIDTH // 2, y + header_height // 2), name, fill='white',
              font=font_medium, anchor='mm')

    # Stats area
    stats_y = y + header_height + 20

    # Cost
    draw.text((x + 20, stats_y), 'Cost:', fill='black', font=font_small, anchor='lm')
    draw.text((x + CARD_WIDTH - 20, stats_y), str(move['cost']), fill='#c0392b',
              font=font_large, anchor='rm')

    # Type
    stats_y += 35
    draw.text((x + 20, stats_y), 'Type:', fill='black', font=font_small, anchor='lm')
    draw.text((x + CARD_WIDTH - 20, stats_y), move['type'], fill='black',
              font=font_small, anchor='rm')

    # Style
    stats_y += 30
    draw.text((x + 20, stats_y), 'Style:', fill='black', font=font_small, anchor='lm')
    style_display = move['style'] if move['style'] else 'Basic'
    draw.text((x + CARD_WIDTH - 20, stats_y), style_display, fill='black',
              font=font_small, anchor='rm')

    # Bonus
    stats_y += 35
    draw.rectangle([x + 10, stats_y - 5, x + CARD_WIDTH - 10, stats_y + 30],
                   fill='#e8f5e9', outline='#27ae60', width=1)
    draw.text((x + 20, stats_y + 12), 'Bonus:', fill='black', font=font_small, anchor='lm')
    draw.text((x + CARD_WIDTH - 20, stats_y + 12), f"+{move['bonus']}", fill='#27ae60',
              font=font_medium, anchor='rm')


def create_rhythm_card(draw, x, y, rhythm, font_large, font_medium, font_small):
    """Draw a rhythm card on the sprite sheet"""
    # Card background
    draw.rectangle([x, y, x + CARD_WIDTH, y + CARD_HEIGHT], fill='white', outline='black', width=2)

    # Header
    header_height = 40
    draw.rectangle([x, y, x + CARD_WIDTH, y + header_height], fill='#8E44AD')
    draw.text((x + CARD_WIDTH // 2, y + header_height // 2), rhythm['name'], fill='white',
              font=font_small, anchor='mm')

    # Effect or flavor
    content_y = y + header_height + 30
    if rhythm['effect']:
        # Effect card
        draw.text((x + CARD_WIDTH // 2, content_y), rhythm['effect'], fill='#8E44AD',
                  font=font_medium, anchor='mm')
        if rhythm['condition']:
            draw.text((x + CARD_WIDTH // 2, content_y + 40), rhythm['condition'], fill='#666',
                      font=font_small, anchor='mm')
    else:
        # Blank card with flavor
        draw.text((x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2), rhythm.get('flavor_text', ''),
                  fill='#999', font=font_small, anchor='mm')


def create_judge_card(draw, x, y, judge, font_large, font_medium, font_small):
    """Draw a judge card on the sprite sheet"""
    # Card background
    draw.rectangle([x, y, x + CARD_WIDTH, y + CARD_HEIGHT], fill='#fef9f0', outline='black', width=2)

    # Header
    header_height = 50
    draw.rectangle([x, y, x + CARD_WIDTH, y + header_height], fill='#C0392B')
    draw.text((x + CARD_WIDTH // 2, y + 15), judge['name'], fill='white',
              font=font_medium, anchor='mm')
    draw.text((x + CARD_WIDTH // 2, y + 35), judge['title'], fill='white',
              font=font_small, anchor='mm')

    # Content
    content_y = y + header_height + 15
    line_height = 25

    # Difficulty
    stars = '★' * int(judge['difficulty'])
    draw.text((x + CARD_WIDTH // 2, content_y), stars, fill='#C0392B',
              font=font_medium, anchor='mm')

    # Requirement (wrapped)
    content_y += line_height + 5
    draw.text((x + 10, content_y), 'Requirement:', fill='black', font=font_small, anchor='lm')
    # Note: In production, you'd want to wrap long text properly
    # For now, keeping it simple

    # Reward
    content_y = y + CARD_HEIGHT - 60
    draw.text((x + 10, content_y), f'Reward: +{judge["reward_points"]} pts', fill='#27ae60',
              font=font_small, anchor='lm')


def create_stumble_card(draw, x, y, font_large, font_medium, font_small):
    """Draw a stumble card on the sprite sheet"""
    # Card background
    draw.rectangle([x, y, x + CARD_WIDTH, y + CARD_HEIGHT], fill='white', outline='black', width=2)

    # Header
    header_height = 40
    draw.rectangle([x, y, x + CARD_WIDTH, y + header_height], fill='#34495E')
    draw.text((x + CARD_WIDTH // 2, y + header_height // 2), 'Stumble', fill='white',
              font=font_medium, anchor='mm')

    # Large X
    draw.text((x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2 - 30), '✗', fill='#e74c3c',
              font=font_large, anchor='mm')

    # Stats
    stats_y = y + CARD_HEIGHT // 2 + 20
    draw.text((x + CARD_WIDTH // 2, stats_y), 'Cost: 0', fill='#666',
              font=font_small, anchor='mm')
    draw.text((x + CARD_WIDTH // 2, stats_y + 20), 'No Style • No Type', fill='#666',
              font=font_small, anchor='mm')


def create_card_back(draw, x, y, card_type, font_large, font_medium):
    """Draw a card back on the sprite sheet"""
    back_colors = {
        'move': '#2C3E50',
        'rhythm': '#8E44AD',
        'judge': '#C0392B',
        'stumble': '#34495E',
    }

    color = hex_to_rgb(back_colors.get(card_type, back_colors['move']))
    draw.rectangle([x, y, x + CARD_WIDTH, y + CARD_HEIGHT], fill=color, outline='black', width=2)

    # Text
    draw.text((x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2 - 30), 'Beat by Beat', fill='white',
              font=font_large, anchor='mm')
    draw.text((x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2 + 20), card_type.upper(), fill='white',
              font=font_medium, anchor='mm')


def create_sprite_sheet(cards, card_type, output_path, is_back=False):
    """Create a TTS sprite sheet from a list of cards"""
    try:
        font_large = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 36)
        font_medium = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 20)
        font_small = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 14)
    except:
        # Fallback to default font
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    num_sheets = (len(cards) + CARDS_PER_SHEET - 1) // CARDS_PER_SHEET

    for sheet_num in range(num_sheets):
        img = Image.new('RGB', (SHEET_WIDTH, SHEET_HEIGHT), color='white')
        draw = ImageDraw.Draw(img)

        start_idx = sheet_num * CARDS_PER_SHEET
        end_idx = min(start_idx + CARDS_PER_SHEET, len(cards))

        for i in range(start_idx, end_idx):
            card_idx = i - start_idx
            row = card_idx // CARDS_PER_ROW
            col = card_idx % CARDS_PER_ROW

            x = col * CARD_WIDTH
            y = row * CARD_HEIGHT

            if is_back:
                create_card_back(draw, x, y, card_type, font_large, font_medium)
            else:
                card = cards[i]
                if card_type == 'move':
                    create_move_card(draw, x, y, card, font_large, font_medium, font_small)
                elif card_type == 'rhythm':
                    create_rhythm_card(draw, x, y, card, font_large, font_medium, font_small)
                elif card_type == 'judge':
                    create_judge_card(draw, x, y, card, font_large, font_medium, font_small)
                elif card_type == 'stumble':
                    create_stumble_card(draw, x, y, font_large, font_medium, font_small)

        # Save
        if num_sheets > 1:
            filename = f'{output_path.stem}_{sheet_num + 1}.png'
        else:
            filename = f'{output_path.stem}.png'

        save_path = output_path.parent / filename
        img.save(save_path, 'PNG', optimize=True)
        print(f'Generated: {filename}')

    return num_sheets


def generate_tts_json(card_counts):
    """Generate a JSON file with TTS deck configuration"""
    config = {
        'ObjectStates': [],
        'game': 'Beat by Beat'
    }

    # This is a basic structure - you'd need to fill in proper TTS deck format
    # with face/back URLs, card IDs, etc.

    return config


def main():
    """Generate TTS sprite sheets for all cards"""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'card-data'
    tts_dir = base_dir / 'tts'

    # Create TTS directory
    tts_dir.mkdir(exist_ok=True)

    print('🎭 Beat by Beat - Tabletop Simulator Generator')
    print('=' * 50)
    print()

    # Generate move cards
    print('Generating move card sprites...')
    move_cards = []
    with open(data_dir / 'moves.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['deck_type'] == 'starter':
                for _ in range(5):  # 5 copies
                    move_cards.append(row)
            else:
                move_cards.append(row)

    num_sheets = create_sprite_sheet(move_cards, 'move', tts_dir / 'move-cards')
    create_sprite_sheet([None] * 70, 'move', tts_dir / 'move-backs', is_back=True)

    # Generate rhythm cards
    print('Generating rhythm card sprites...')
    rhythm_cards = []
    with open(data_dir / 'rhythm-cards.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            copies = int(row.get('copies', 1))
            for _ in range(copies):
                rhythm_cards.append(row)

    create_sprite_sheet(rhythm_cards, 'rhythm', tts_dir / 'rhythm-cards')
    create_sprite_sheet([None] * 70, 'rhythm', tts_dir / 'rhythm-backs', is_back=True)

    # Generate judge cards
    print('Generating judge card sprites...')
    judge_cards = []
    with open(data_dir / 'judge-cards.csv', 'r') as f:
        reader = csv.DictReader(f)
        judge_cards = list(reader)

    create_sprite_sheet(judge_cards, 'judge', tts_dir / 'judge-cards')
    create_sprite_sheet([None] * 70, 'judge', tts_dir / 'judge-backs', is_back=True)

    # Generate stumble cards
    print('Generating stumble card sprites...')
    stumble_cards = [{}] * 20  # 20 stumble cards

    create_sprite_sheet(stumble_cards, 'stumble', tts_dir / 'stumble-cards')
    create_sprite_sheet([None] * 70, 'stumble', tts_dir / 'stumble-backs', is_back=True)

    print()
    print(f'✅ TTS sprite sheets generated in: {tts_dir}')
    print()
    print('To use in Tabletop Simulator:')
    print('1. Upload the PNG files to Imgur or another image host')
    print('2. In TTS, create a Custom Deck')
    print('3. Use the image URLs for Face and Back')
    print('4. Set deck type to Custom (10x7)')
    print()


if __name__ == '__main__':
    main()
