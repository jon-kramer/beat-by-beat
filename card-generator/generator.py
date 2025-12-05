#!/usr/bin/env python3
"""
Beat by Beat Card Generator
Generates printable HTML sheets of cards from CSV data
"""

import csv
import os
from pathlib import Path

# Color scheme for styles
COLORS = {
    'Latin': '#FF6B6B',           # Coral
    'Ballroom': '#6B5B95',        # Deep Indigo
    'Classical': '#8FB996',       # Soft Sage
    'Jazz': '#E9C46A',            # Warm Gold
    'Street': '#457B9D',          # Slate Blue
    'Styleless': '#B8B8B8',       # Light Gray (changed from cream for contrast)
}

# Type icons (simple SVG paths for placeholder graphics)
TYPE_ICONS = {
    'Step': '''<svg viewBox="0 0 100 100" class="type-icon">
        <path d="M30,50 L50,30 L70,50 L50,70 Z" fill="currentColor"/>
        <circle cx="30" cy="70" r="8" fill="currentColor"/>
        <circle cx="70" cy="70" r="8" fill="currentColor"/>
    </svg>''',

    'Spin': '''<svg viewBox="0 0 100 100" class="type-icon">
        <path d="M50,20 Q80,50 50,80 Q20,50 50,20" fill="none" stroke="currentColor" stroke-width="4"/>
        <circle cx="50" cy="50" r="6" fill="currentColor"/>
        <path d="M70,35 L85,30 L80,45" fill="currentColor"/>
    </svg>''',

    'Jump': '''<svg viewBox="0 0 100 100" class="type-icon">
        <path d="M50,20 L60,40 L50,35 L40,40 Z" fill="currentColor"/>
        <path d="M30,60 L50,45 L70,60" stroke="currentColor" stroke-width="4" fill="none"/>
        <line x1="30" y1="60" x2="30" y2="80" stroke="currentColor" stroke-width="3"/>
        <line x1="70" y1="60" x2="70" y2="80" stroke="currentColor" stroke-width="3"/>
    </svg>''',

    'Pose': '''<svg viewBox="0 0 100 100" class="type-icon">
        <circle cx="50" cy="30" r="12" fill="currentColor"/>
        <line x1="50" y1="42" x2="50" y2="65" stroke="currentColor" stroke-width="4"/>
        <line x1="50" y1="50" x2="30" y2="60" stroke="currentColor" stroke-width="4"/>
        <line x1="50" y1="50" x2="70" y2="40" stroke="currentColor" stroke-width="4"/>
        <line x1="50" y1="65" x2="35" y2="85" stroke="currentColor" stroke-width="4"/>
        <line x1="50" y1="65" x2="65" y2="85" stroke="currentColor" stroke-width="4"/>
    </svg>''',

    'Flow': '''<svg viewBox="0 0 100 100" class="type-icon">
        <path d="M10,50 Q30,20 50,50 T90,50" fill="none" stroke="currentColor" stroke-width="4"/>
        <path d="M10,60 Q30,80 50,60 T90,60" fill="none" stroke="currentColor" stroke-width="3" opacity="0.6"/>
    </svg>''',

    'Pop': '''<svg viewBox="0 0 100 100" class="type-icon">
        <rect x="35" y="35" width="30" height="30" fill="currentColor"/>
        <path d="M20,20 L30,30 M80,20 L70,30 M20,80 L30,70 M80,80 L70,70" stroke="currentColor" stroke-width="3"/>
        <circle cx="20" cy="20" r="4" fill="currentColor"/>
        <circle cx="80" cy="20" r="4" fill="currentColor"/>
        <circle cx="20" cy="80" r="4" fill="currentColor"/>
        <circle cx="80" cy="80" r="4" fill="currentColor"/>
    </svg>''',
}

# Recovery action icons and descriptions
RECOVERY_ACTIONS = {
    'Stamina': {
        'icon': '''<svg viewBox="0 0 100 100" class="recovery-icon">
            <circle cx="50" cy="50" r="35" fill="none" stroke="currentColor" stroke-width="6"/>
            <path d="M30,50 L45,35 L45,65 Z" fill="currentColor"/>
            <path d="M70,50 L55,35 L55,65 Z" fill="currentColor"/>
        </svg>''',
        'description': 'Recover 1 Stamina'
    },
    'Inspiration': {
        'icon': '''<svg viewBox="0 0 100 100" class="recovery-icon">
            <path d="M50,15 L58,45 L88,45 L63,63 L73,93 L50,75 L27,93 L37,63 L12,45 L42,45 Z" fill="currentColor"/>
        </svg>''',
        'description': 'Draw 1 card'
    },
    'Refinement': {
        'icon': '''<svg viewBox="0 0 100 100" class="recovery-icon">
            <rect x="20" y="20" width="60" height="60" fill="none" stroke="currentColor" stroke-width="6" rx="5"/>
            <line x1="30" y1="30" x2="70" y2="70" stroke="currentColor" stroke-width="6"/>
            <line x1="70" y1="30" x2="30" y2="70" stroke="currentColor" stroke-width="6"/>
        </svg>''',
        'description': 'Discard & redraw 1'
    },
}


def get_style_color(style):
    """Get the color for a style (or blend colors for multi-style)"""
    if not style:
        return COLORS['Styleless']

    styles = [s.strip() for s in style.split('/')]
    if len(styles) == 1:
        return COLORS.get(styles[0], COLORS['Styleless'])
    else:
        # For multi-style, return a gradient
        color1 = COLORS.get(styles[0], COLORS['Styleless'])
        color2 = COLORS.get(styles[1], COLORS['Styleless'])
        return f"linear-gradient(135deg, {color1} 0%, {color2} 100%)"


def generate_move_card(move, card_num):
    """Generate HTML for a single move card"""
    style_bg = get_style_color(move['style'])
    is_gradient = 'gradient' in style_bg

    style_attr = f'background: {style_bg};' if is_gradient else f'background-color: {style_bg};'

    type_icon = TYPE_ICONS.get(move['type'], '')
    recovery_action = move.get('recovery_action', 'Stamina')
    recovery_data = RECOVERY_ACTIONS.get(recovery_action, RECOVERY_ACTIONS['Stamina'])
    recovery_icon = recovery_data['icon']
    recovery_desc = recovery_data['description']

    style_display = move['style'] if move['style'] else 'Basic'

    return f'''
    <div class="card move-card">
        <div class="card-header" style="{style_attr}">
            <div class="card-name">{move['name']}</div>
        </div>
        <div class="card-body">
            <div class="card-image">
                {type_icon}
            </div>
            <div class="card-stats">
                <div class="stat-row technique-row">
                    <span class="stat-label">Technique</span>
                    <span class="stat-value technique-value">{move['cost']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Type</span>
                    <span class="stat-value">{move['type']}</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Style</span>
                    <span class="stat-value">{style_display}</span>
                </div>
                <div class="stat-row bonus-row">
                    <span class="stat-label">Bonus</span>
                    <span class="stat-value bonus-value">+{move['bonus']}</span>
                </div>
                <div class="stat-row recovery-row">
                    <span class="stat-label-recovery">{recovery_icon}</span>
                    <span class="stat-value recovery-value">{recovery_desc}</span>
                </div>
            </div>
        </div>
    </div>'''


def generate_rhythm_card(rhythm):
    """Generate HTML for a single rhythm card"""
    is_blank = not rhythm['effect']

    return f'''
    <div class="card rhythm-card {'blank-rhythm' if is_blank else ''}">
        <div class="card-header rhythm-header">
            <div class="card-name">{rhythm['name']}</div>
        </div>
        <div class="card-body rhythm-body">
            {f'<div class="rhythm-effect">{rhythm["effect"]}</div>' if rhythm['effect'] else ''}
            {f'<div class="rhythm-condition">{rhythm["condition"]}</div>' if rhythm['condition'] else ''}
            {f'<div class="rhythm-flavor">{rhythm["flavor_text"]}</div>' if rhythm.get('flavor_text') else ''}
        </div>
    </div>'''


def generate_judge_card(judge):
    """Generate HTML for a single judge card"""
    stars = '★' * int(judge['difficulty'])

    return f'''
    <div class="card judge-card">
        <div class="card-header judge-header">
            <div class="judge-name">{judge['name']}</div>
            <div class="judge-title">{judge['title']}</div>
            <div class="judge-difficulty">{stars}</div>
        </div>
        <div class="card-body judge-body">
            <div class="judge-quote">"{judge['flavor_quote']}"</div>
            <div class="judge-requirement">
                <strong>Requirement:</strong><br/>
                {judge['requirement']}
            </div>
            <div class="judge-reward">
                <strong>Reward:</strong> +{judge['reward_points']} points
            </div>
            <div class="judge-ongoing">
                <strong>Ongoing:</strong><br/>
                {judge['ongoing_effect']}
            </div>
        </div>
    </div>'''


def generate_stumble_card():
    """Generate HTML for a stumble card - matches move card layout"""
    stumble_icon = '''<svg viewBox="0 0 100 100" class="type-icon">
        <line x1="20" y1="20" x2="80" y2="80" stroke="currentColor" stroke-width="8"/>
        <line x1="80" y1="20" x2="20" y2="80" stroke="currentColor" stroke-width="8"/>
        <circle cx="50" cy="50" r="35" fill="none" stroke="currentColor" stroke-width="6"/>
    </svg>'''

    return f'''
    <div class="card move-card stumble-card">
        <div class="card-header stumble-header">
            <div class="card-name">Stumble</div>
        </div>
        <div class="card-body">
            <div class="card-image">
                {stumble_icon}
            </div>
            <div class="card-stats">
                <div class="stat-row technique-row">
                    <span class="stat-label">Technique</span>
                    <span class="stat-value technique-value">0</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Type</span>
                    <span class="stat-value stumble-text">—</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Style</span>
                    <span class="stat-value stumble-text">—</span>
                </div>
                <div class="stat-row bonus-row stumble-bonus-row">
                    <span class="stat-label">Bonus</span>
                    <span class="stat-value bonus-value stumble-text">+0</span>
                </div>
                <div class="stat-row stumble-penalty-row">
                    <span class="stat-value stumble-penalty">Lose your rhythm</span>
                </div>
            </div>
        </div>
    </div>'''


def generate_card_back(card_type):
    """Generate HTML for a card back"""
    back_colors = {
        'move': '#2C3E50',
        'rhythm': '#8E44AD',
        'judge': '#C0392B',
        'stumble': '#34495E',
    }

    return f'''
    <div class="card card-back {card_type}-back" style="background-color: {back_colors[card_type]};">
        <div class="back-content">
            <div class="back-title">Beat by Beat</div>
            <div class="back-type">{card_type.title()}</div>
        </div>
    </div>'''


def generate_css():
    """Generate the CSS stylesheet"""
    return '''
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    background: #f0f0f0;
    padding: 0;
    margin: 0;
}

.sheet {
    width: 8.5in;
    height: 11in;
    background: white;
    margin: 0 auto;
    page-break-after: always;
    display: grid;
    grid-template-columns: repeat(3, 2.5in);
    grid-template-rows: repeat(3, 3.5in);
    padding: 0.25in;
    gap: 0.125in;
}

.card {
    width: 2.5in;
    height: 3.5in;
    border: 2px solid #333;
    border-radius: 0.15in;
    overflow: hidden;
    background: white;
    display: flex;
    flex-direction: column;
    position: relative;
}

/* Move Cards */
.move-card .card-header {
    padding: 0.15in;
    color: white;
    text-align: center;
    min-height: 0.5in;
    display: flex;
    align-items: center;
    justify-content: center;
}

.move-card .card-name {
    font-size: 14pt;
    font-weight: bold;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
}

.move-card .card-body {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0.08in;
}

.move-card .card-image {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0.05in 0;
}

.type-icon {
    width: 0.8in;
    height: 0.8in;
    opacity: 0.7;
}

.move-card .card-stats {
    display: flex;
    flex-direction: column;
    gap: 0.05in;
}

.stat-row {
    display: flex;
    justify-content: space-between;
    font-size: 9pt;
    padding: 0.04in 0.08in;
    border-radius: 0.05in;
    background: #f8f8f8;
}

.stat-label {
    font-weight: bold;
    color: #555;
}

.stat-value {
    color: #222;
}

.technique-row {
    background: #e8e8e8;
}

.technique-value {
    font-size: 12pt;
    font-weight: bold;
    color: #c0392b;
}

.bonus-row {
    background: #e8f5e9;
}

.bonus-value {
    font-size: 11pt;
    font-weight: bold;
    color: #27ae60;
}

.recovery-row {
    background: #e3f2fd;
    display: flex;
    align-items: center;
    gap: 0.05in;
}

.stat-label-recovery {
    flex-shrink: 0;
}

.recovery-icon {
    width: 0.25in;
    height: 0.25in;
    color: #1976d2;
}

.recovery-value {
    font-size: 8pt;
    font-weight: bold;
    color: #1565c0;
    flex: 1;
}

/* Rhythm Cards */
.rhythm-card .card-header {
    padding: 0.15in;
    background: #8E44AD;
    color: white;
    text-align: center;
}

.rhythm-card .card-name {
    font-size: 12pt;
    font-weight: bold;
}

.rhythm-card .card-body {
    flex: 1;
    padding: 0.15in;
    display: flex;
    flex-direction: column;
    gap: 0.1in;
}

.rhythm-effect {
    font-size: 14pt;
    font-weight: bold;
    color: #8E44AD;
    text-align: center;
}

.rhythm-condition {
    font-size: 9pt;
    color: #555;
    font-style: italic;
    text-align: center;
}

.rhythm-flavor {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10pt;
    color: #666;
    font-style: italic;
    text-align: center;
    padding: 0.15in;
}

.blank-rhythm .rhythm-flavor {
    font-size: 12pt;
}

/* Judge Cards */
.judge-card {
    background: linear-gradient(to bottom, #fff 0%, #fef9f0 100%);
}

.judge-card .card-header {
    padding: 0.15in;
    background: #C0392B;
    color: white;
}

.judge-name {
    font-size: 13pt;
    font-weight: bold;
}

.judge-title {
    font-size: 9pt;
    font-style: italic;
    opacity: 0.9;
}

.judge-difficulty {
    font-size: 10pt;
    margin-top: 0.05in;
}

.judge-card .card-body {
    flex: 1;
    padding: 0.12in;
    display: flex;
    flex-direction: column;
    gap: 0.08in;
    font-size: 8pt;
}

.judge-quote {
    font-style: italic;
    color: #666;
    text-align: center;
    padding-bottom: 0.08in;
    border-bottom: 1px solid #ddd;
}

.judge-requirement {
    font-size: 8pt;
    line-height: 1.3;
}

.judge-reward {
    font-size: 9pt;
    font-weight: bold;
    color: #27ae60;
}

.judge-ongoing {
    font-size: 8pt;
    line-height: 1.3;
    flex: 1;
}

/* Stumble Cards */
.stumble-header {
    background: #5A5A5A !important;
    color: white;
}

.stumble-text {
    color: #999;
}

.stumble-bonus-row {
    background: #f0f0f0 !important;
}

.stumble-penalty-row {
    background: #FFE6E6;
    justify-content: center;
    padding: 0.06in 0.08in;
}

.stumble-penalty {
    font-size: 9pt;
    font-weight: bold;
    color: #c0392b;
    font-style: italic;
    text-align: center;
}

/* Card Backs */
.card-back {
    display: flex;
    align-items: center;
    justify-content: center;
}

.back-content {
    text-align: center;
    color: white;
}

.back-title {
    font-size: 18pt;
    font-weight: bold;
    margin-bottom: 0.2in;
}

.back-type {
    font-size: 14pt;
    text-transform: uppercase;
    letter-spacing: 0.05in;
}

/* Print Styles */
@media print {
    body {
        margin: 0;
        padding: 0;
    }

    .sheet {
        margin: 0;
        padding: 0.25in;
    }

    @page {
        size: letter;
        margin: 0;
    }
}
'''


def generate_html_document(all_sheets, card_type):
    """Generate a complete HTML document with multiple sheets"""
    css = generate_css()

    sheets_html = []
    for sheet_cards in all_sheets:
        sheets_html.append(f'''    <div class="sheet">
        {''.join(sheet_cards)}
    </div>''')

    return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Beat by Beat - {card_type.title()} Cards</title>
    <style>{css}</style>
</head>
<body>
{''.join(sheets_html)}
</body>
</html>'''


def main():
    """Main generator function"""
    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'card-data'
    output_dir = base_dir / 'output' / 'html'

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    cards_per_sheet = 9

    # Generate move cards (including 5 copies of starter deck)
    move_cards = []
    with open(data_dir / 'moves.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['deck_type'] == 'starter':
                # Generate 5 copies for 5 players
                for _ in range(5):
                    move_cards.append(generate_move_card(row, len(move_cards)))
            else:
                move_cards.append(generate_move_card(row, len(move_cards)))

    # Split into sheets
    move_sheets = []
    for i in range(0, len(move_cards), cards_per_sheet):
        sheet_cards = move_cards[i:i + cards_per_sheet]
        # Pad with empty divs if needed
        while len(sheet_cards) < cards_per_sheet:
            sheet_cards.append('<div></div>')
        move_sheets.append(sheet_cards)

    # Generate single HTML file with all move cards
    html = generate_html_document(move_sheets, 'move')
    output_file = output_dir / 'move-cards.html'
    with open(output_file, 'w') as f:
        f.write(html)
    print(f'Generated: {output_file.name} ({len(move_sheets)} sheets)')

    # Generate rhythm cards
    rhythm_cards = []
    with open(data_dir / 'rhythm-cards.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            copies = int(row.get('copies', 1))
            for _ in range(copies):
                rhythm_cards.append(generate_rhythm_card(row))

    rhythm_sheets = []
    for i in range(0, len(rhythm_cards), cards_per_sheet):
        sheet_cards = rhythm_cards[i:i + cards_per_sheet]
        while len(sheet_cards) < cards_per_sheet:
            sheet_cards.append('<div></div>')
        rhythm_sheets.append(sheet_cards)

    html = generate_html_document(rhythm_sheets, 'rhythm')
    output_file = output_dir / 'rhythm-cards.html'
    with open(output_file, 'w') as f:
        f.write(html)
    print(f'Generated: {output_file.name} ({len(rhythm_sheets)} sheets)')

    # Generate judge cards
    judge_cards = []
    with open(data_dir / 'judge-cards.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            judge_cards.append(generate_judge_card(row))

    judge_sheets = []
    for i in range(0, len(judge_cards), cards_per_sheet):
        sheet_cards = judge_cards[i:i + cards_per_sheet]
        while len(sheet_cards) < cards_per_sheet:
            sheet_cards.append('<div></div>')
        judge_sheets.append(sheet_cards)

    html = generate_html_document(judge_sheets, 'judge')
    output_file = output_dir / 'judge-cards.html'
    with open(output_file, 'w') as f:
        f.write(html)
    print(f'Generated: {output_file.name} ({len(judge_sheets)} sheets)')

    # Generate stumble cards
    stumble_cards = [generate_stumble_card() for _ in range(20)]

    stumble_sheets = []
    for i in range(0, len(stumble_cards), cards_per_sheet):
        sheet_cards = stumble_cards[i:i + cards_per_sheet]
        while len(sheet_cards) < cards_per_sheet:
            sheet_cards.append('<div></div>')
        stumble_sheets.append(sheet_cards)

    html = generate_html_document(stumble_sheets, 'stumble')
    output_file = output_dir / 'stumble-cards.html'
    with open(output_file, 'w') as f:
        f.write(html)
    print(f'Generated: {output_file.name} ({len(stumble_sheets)} sheets)')

    # Generate card backs (one sheet for each type)
    for card_type in ['move', 'rhythm', 'judge', 'stumble']:
        backs = [generate_card_back(card_type) for _ in range(cards_per_sheet)]
        html = generate_html_document([backs], f'{card_type}-back')
        output_file = output_dir / f'{card_type}-backs.html'
        with open(output_file, 'w') as f:
            f.write(html)
        print(f'Generated: {output_file.name}')

    print(f'\nTotal move cards: {len(move_cards)}')
    print(f'Total rhythm cards: {len(rhythm_cards)}')
    print(f'Total judge cards: {len(judge_cards)}')
    print(f'Total stumble cards: {len(stumble_cards)}')
    print(f'\nAll cards generated in: {output_dir}')


if __name__ == '__main__':
    main()
