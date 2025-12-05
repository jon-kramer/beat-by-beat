#!/usr/bin/env python3
"""
TTS JSON Save File Generator for Beat by Beat
Generates a Tabletop Simulator save file with all card decks pre-configured
"""

import json
import re
from pathlib import Path


def get_github_info():
    """Extract GitHub username and repo from git remote"""
    import subprocess

    try:
        result = subprocess.run(
            ['git', 'config', '--get', 'remote.origin.url'],
            capture_output=True,
            text=True,
            check=True
        )

        remote_url = result.stdout.strip()

        # Parse GitHub URL (supports both HTTPS and SSH)
        match = re.search(r'github\.com[:/]([^/]+)/([^/.]+)', remote_url)
        if match:
            username = match.group(1)
            repo = match.group(2)
            return username, repo
        else:
            raise ValueError(f"Could not parse GitHub URL: {remote_url}")

    except subprocess.CalledProcessError:
        raise ValueError("No git remote found. Run this after setting up GitHub.")


def get_github_raw_url(username, repo, branch, filepath):
    """Generate GitHub raw URL for a file"""
    return f"https://raw.githubusercontent.com/{username}/{repo}/{branch}/output/tts/{filepath}"


def find_tts_files(tts_dir):
    """Find all TTS sprite sheet PNG files"""
    files = {
        'move_fronts': [],
        'move_back': None,
        'rhythm_fronts': [],
        'rhythm_back': None,
        'judge_fronts': [],
        'judge_back': None,
        'stumble_fronts': [],
        'stumble_back': None,
    }

    for png_file in sorted(tts_dir.glob('*.png')):
        name = png_file.name

        if 'move-cards' in name and 'back' not in name:
            files['move_fronts'].append(name)
        elif 'move-backs' in name:
            files['move_back'] = name
        elif 'rhythm-cards' in name and 'back' not in name:
            files['rhythm_fronts'].append(name)
        elif 'rhythm-backs' in name:
            files['rhythm_back'] = name
        elif 'judge-cards' in name and 'back' not in name:
            files['judge_fronts'].append(name)
        elif 'judge-backs' in name:
            files['judge_back'] = name
        elif 'stumble-cards' in name and 'back' not in name:
            files['stumble_fronts'].append(name)
        elif 'stumble-backs' in name:
            files['stumble_back'] = name

    return files


def calculate_grid_size(num_cards):
    """Calculate NumWidth and NumHeight based on actual number of cards"""
    import math

    # TTS uses 10x7 grid, but we need to report actual dimensions
    cards_per_row = 10
    num_rows = math.ceil(num_cards / cards_per_row)

    # For last row, calculate actual width
    cards_in_last_row = num_cards % cards_per_row
    if cards_in_last_row == 0:
        cards_in_last_row = cards_per_row

    # Return width (10 for full grid) and height (actual rows)
    return cards_per_row, num_rows


def create_deck_object(name, face_url, back_url, num_cards, position, description="", deck_id=1):
    """Create a TTS deck object with proper configuration"""

    # Generate unique GUID for this deck
    import hashlib
    guid = hashlib.md5(f"{name}{position[0]}{position[2]}".encode()).hexdigest()[:6]

    # Calculate proper grid dimensions
    num_width, num_height = calculate_grid_size(num_cards)

    return {
        "Name": "DeckCustom",
        "Transform": {
            "posX": position[0],
            "posY": position[1],
            "posZ": position[2],
            "rotX": 0.0,
            "rotY": 180.0,
            "rotZ": 0.0,
            "scaleX": 1.0,
            "scaleY": 1.0,
            "scaleZ": 1.0
        },
        "Nickname": name,
        "Description": description,
        "GMNotes": "",
        "ColorDiffuse": {
            "r": 0.713235259,
            "g": 0.713235259,
            "b": 0.713235259
        },
        "LayoutGroupSortIndex": 0,
        "Value": 0,
        "Locked": False,
        "Grid": True,
        "Snap": True,
        "IgnoreFoW": False,
        "MeasureMovement": False,
        "DragSelectable": True,
        "Autoraise": True,
        "Sticky": True,
        "Tooltip": True,
        "GridProjection": False,
        "HideWhenFaceDown": True,
        "Hands": True,
        "SidewaysCard": False,
        "DeckIDs": list(range(deck_id * 100, deck_id * 100 + num_cards)),
        "CustomDeck": {
            str(deck_id): {
                "FaceURL": face_url,
                "BackURL": back_url,
                "NumWidth": num_width,
                "NumHeight": num_height,
                "BackIsHidden": True,
                "UniqueBack": False,
                "Type": 0
            }
        },
        "LuaScript": "",
        "LuaScriptState": "",
        "XmlUI": "",
        "GUID": guid
    }


def count_cards_in_csv(csv_path, filter_fn=None):
    """Count cards in a CSV file with optional filter"""
    import csv
    count = 0
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if filter_fn is None or filter_fn(row):
                copies = int(row.get('copies', 1))
                count += copies
    return count


def generate_tts_save(username, repo, tts_files, branch="main"):
    """Generate complete TTS save file JSON"""
    from pathlib import Path
    import csv

    base_dir = Path(__file__).parent.parent
    data_dir = base_dir / 'card-data'

    objects = []
    deck_id_counter = 1

    # Starting position for first deck
    x, y, z = 0, 1, 0
    spacing = 4.5  # Space between decks

    # Count starter vs pool move cards
    starter_count = 0
    pool_count = 0
    with open(data_dir / 'moves.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['deck_type'] == 'starter':
                starter_count += 5  # 5 copies per player
            else:
                pool_count += 1

    total_move_count = starter_count + pool_count

    # STARTER DECK (first 55 cards from sheet 1)
    face_url = get_github_raw_url(username, repo, branch, tts_files['move_fronts'][0])
    back_url = get_github_raw_url(username, repo, branch, tts_files['move_back'])

    starter_deck = create_deck_object(
        name="Starter Move Cards (5 Players)",
        face_url=face_url,
        back_url=back_url,
        num_cards=starter_count,  # 55 starter cards
        position=[x, y, z],
        description="Starting deck - Deal 11 cards to each of 5 players",
        deck_id=deck_id_counter
    )
    objects.append(starter_deck)
    x += spacing
    deck_id_counter += 1

    # POOL MOVE DECKS (remaining sheets)
    # Calculate cards per sheet
    cards_processed = starter_count
    for i, front_file in enumerate(tts_files['move_fronts']):
        if cards_processed >= total_move_count:
            break

        # Calculate how many cards are on this sheet
        cards_remaining = total_move_count - cards_processed
        cards_on_sheet = min(70, cards_remaining)

        # Skip starter cards on first sheet
        if i == 0:
            cards_on_sheet = min(70 - starter_count, pool_count)
            cards_processed += cards_on_sheet

            if cards_on_sheet > 0:
                face_url = get_github_raw_url(username, repo, branch, front_file)
                deck = create_deck_object(
                    name=f"Pool Move Cards {i + 1}",
                    face_url=face_url,
                    back_url=back_url,
                    num_cards=cards_on_sheet,
                    position=[x, y, z],
                    description="Advanced move cards for drafting",
                    deck_id=deck_id_counter
                )
                objects.append(deck)
                x += spacing
                deck_id_counter += 1
        else:
            cards_processed += cards_on_sheet
            face_url = get_github_raw_url(username, repo, branch, front_file)
            deck = create_deck_object(
                name=f"Pool Move Cards {i + 1}",
                face_url=face_url,
                back_url=back_url,
                num_cards=cards_on_sheet,
                position=[x, y, z],
                description="Advanced move cards for drafting",
                deck_id=deck_id_counter
            )
            objects.append(deck)
            x += spacing
            deck_id_counter += 1

    # Rhythm card decks
    rhythm_count = count_cards_in_csv(data_dir / 'rhythm-cards.csv')
    cards_processed = 0

    for i, front_file in enumerate(tts_files['rhythm_fronts'], 1):
        cards_remaining = rhythm_count - cards_processed
        cards_on_sheet = min(70, cards_remaining)
        cards_processed += cards_on_sheet

        face_url = get_github_raw_url(username, repo, branch, front_file)
        back_url = get_github_raw_url(username, repo, branch, tts_files['rhythm_back'])

        deck = create_deck_object(
            name=f"Rhythm Cards {i}" if len(tts_files['rhythm_fronts']) > 1 else "Rhythm Cards",
            face_url=face_url,
            back_url=back_url,
            num_cards=cards_on_sheet,
            position=[x, y, z],
            description=f"Rhythm cards - Sheet {i}",
            deck_id=deck_id_counter
        )
        objects.append(deck)
        x += spacing
        deck_id_counter += 1

    # Judge cards
    if tts_files['judge_fronts']:
        judge_count = count_cards_in_csv(data_dir / 'judge-cards.csv')
        face_url = get_github_raw_url(username, repo, branch, tts_files['judge_fronts'][0])
        back_url = get_github_raw_url(username, repo, branch, tts_files['judge_back'])

        deck = create_deck_object(
            name="Judge Cards",
            face_url=face_url,
            back_url=back_url,
            num_cards=judge_count,
            position=[x, y, z],
            description="Judge cards with special requirements",
            deck_id=deck_id_counter
        )
        objects.append(deck)
        x += spacing
        deck_id_counter += 1

    # Stumble cards
    if tts_files['stumble_fronts']:
        face_url = get_github_raw_url(username, repo, branch, tts_files['stumble_fronts'][0])
        back_url = get_github_raw_url(username, repo, branch, tts_files['stumble_back'])

        deck = create_deck_object(
            name="Stumble Cards",
            face_url=face_url,
            back_url=back_url,
            num_cards=20,
            position=[x, y, z],
            description="Stumble penalty cards",
            deck_id=deck_id_counter
        )
        objects.append(deck)
        deck_id_counter += 1

    # Complete TTS save file structure
    save_data = {
        "SaveName": "Beat by Beat",
        "GameMode": "Free",
        "Gravity": 0.5,
        "PlayArea": 0.5,
        "Date": "",
        "Table": "Table_None",
        "Sky": "Sky_Museum",
        "Note": "",
        "Rules": "",
        "XmlUI": "",
        "LuaScript": "",
        "LuaScriptState": "",
        "ObjectStates": objects,
        "TabStates": {},
        "VersionNumber": "v13.2.2"
    }

    return save_data


def main():
    """Generate TTS save file from GitHub-hosted sprites"""
    base_dir = Path(__file__).parent.parent
    tts_dir = base_dir / 'output' / 'tts'

    print('🎮 Beat by Beat - TTS JSON Generator')
    print('=' * 50)
    print()

    # Check TTS files exist
    if not tts_dir.exists():
        print('❌ Error: output/tts/ directory not found')
        print('   Run ./scripts/generate-all.sh first')
        return 1

    # Get GitHub info
    try:
        username, repo = get_github_info()
        print(f'📍 GitHub: {username}/{repo}')
    except ValueError as e:
        print(f'❌ Error: {e}')
        return 1

    # Find TTS files
    tts_files = find_tts_files(tts_dir)

    print(f'📦 Found sprite sheets:')
    print(f'  - Move cards: {len(tts_files["move_fronts"])} sheet(s)')
    print(f'  - Rhythm cards: {len(tts_files["rhythm_fronts"])} sheet(s)')
    print(f'  - Judge cards: {len(tts_files["judge_fronts"])} sheet(s)')
    print(f'  - Stumble cards: {len(tts_files["stumble_fronts"])} sheet(s)')
    print()

    # Generate save file
    print('🔨 Generating TTS save file...')
    save_data = generate_tts_save(username, repo, tts_files)

    # Write JSON
    output_file = tts_dir / 'beat-by-beat.json'
    with open(output_file, 'w') as f:
        json.dump(save_data, f, indent=2)

    print(f'✅ Generated: {output_file.name}')
    print()
    print('📋 To import into Tabletop Simulator:')
    print('  1. In TTS: Objects → Saved Objects → Import')
    print(f'  2. Select: {output_file}')
    print('  3. All decks will spawn on the table!')
    print()
    print('💡 Note: Make sure you\'ve pushed to GitHub first.')
    print('   Images must be available at GitHub raw URLs.')
    print()

    return 0


if __name__ == '__main__':
    exit(main())
