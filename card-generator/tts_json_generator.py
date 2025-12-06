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
        'starter_fronts': [],
        'pool_fronts': [],
        'move_back': None,
        'rhythm_fronts': [],
        'rhythm_back': None,
        'judge_fronts': [],
        'judge_back': None,
        'stumble_fronts': [],
    }

    for png_file in sorted(tts_dir.glob('*.png')):
        name = png_file.name

        if 'starter-cards' in name and 'back' not in name:
            files['starter_fronts'].append(name)
        elif 'pool-cards' in name and 'back' not in name:
            files['pool_fronts'].append(name)
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

    return files


def calculate_grid_size(num_cards):
    """Calculate NumWidth and NumHeight - always 10x7 for consistency"""
    # TTS sprite sheets are ALWAYS rendered as 10x7 grids (70 cards)
    # Even if there are fewer cards, we pad with empty spaces
    # This ensures consistent dimensions and proper card sizing in TTS
    return 10, 7


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
                "UniqueBack": True,
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

    # Count starter and pool move cards
    starter_count = count_cards_in_csv(data_dir / 'moves.csv', lambda row: row['deck_type'] == 'starter')
    pool_count = count_cards_in_csv(data_dir / 'moves.csv', lambda row: row['deck_type'] == 'pool')

    back_url = get_github_raw_url(username, repo, branch, tts_files['move_back'])

    # STARTER DECK (single copies - user will duplicate)
    if tts_files['starter_fronts']:
        face_url = get_github_raw_url(username, repo, branch, tts_files['starter_fronts'][0])

        starter_deck = create_deck_object(
            name="Starter Move Cards",
            face_url=face_url,
            back_url=back_url,
            num_cards=starter_count,
            position=[x, y, z],
            description="Starting cards - Print/duplicate 5 times for 5 players",
            deck_id=deck_id_counter
        )
        objects.append(starter_deck)
        x += spacing
        deck_id_counter += 1

    # POOL MOVE DECK (combined into one deck from all sheets)
    if tts_files['pool_fronts']:
        # Combine all pool card sheets into a single deck
        all_deck_ids = []
        custom_decks = {}

        cards_processed = 0
        for i, front_file in enumerate(tts_files['pool_fronts'], start=1):
            cards_remaining = pool_count - cards_processed
            cards_on_sheet = min(70, cards_remaining)

            # Add deck IDs for this sheet
            start_id = deck_id_counter * 100
            all_deck_ids.extend(range(start_id, start_id + cards_on_sheet))

            # Add custom deck entry
            face_url = get_github_raw_url(username, repo, branch, front_file)
            num_width, num_height = calculate_grid_size(cards_on_sheet)

            custom_decks[str(deck_id_counter)] = {
                "FaceURL": face_url,
                "BackURL": back_url,
                "NumWidth": num_width,
                "NumHeight": num_height,
                "BackIsHidden": True,
                "UniqueBack": True,
                "Type": 0
            }

            cards_processed += cards_on_sheet
            deck_id_counter += 1

        # Create single combined pool deck
        import hashlib
        guid = hashlib.md5(f"pool{x}{z}".encode()).hexdigest()[:6]

        pool_deck = {
            "Name": "DeckCustom",
            "Transform": {
                "posX": x,
                "posY": y,
                "posZ": z,
                "rotX": 0.0,
                "rotY": 180.0,
                "rotZ": 0.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            "Nickname": "Pool Move Cards",
            "Description": "Advanced move cards for drafting",
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
            "DeckIDs": all_deck_ids,
            "CustomDeck": custom_decks,
            "LuaScript": "",
            "LuaScriptState": "",
            "XmlUI": "",
            "GUID": guid
        }
        objects.append(pool_deck)
        x += spacing

    # Rhythm card deck (combined into one deck from all sheets)
    if tts_files['rhythm_fronts']:
        rhythm_count = count_cards_in_csv(data_dir / 'rhythm-cards.csv')
        back_url = get_github_raw_url(username, repo, branch, tts_files['rhythm_back'])

        # Combine all rhythm card sheets into a single deck
        all_deck_ids = []
        custom_decks = {}

        cards_processed = 0
        for i, front_file in enumerate(tts_files['rhythm_fronts'], start=1):
            cards_remaining = rhythm_count - cards_processed
            cards_on_sheet = min(70, cards_remaining)

            # Add deck IDs for this sheet
            start_id = deck_id_counter * 100
            all_deck_ids.extend(range(start_id, start_id + cards_on_sheet))

            # Add custom deck entry
            face_url = get_github_raw_url(username, repo, branch, front_file)
            num_width, num_height = calculate_grid_size(cards_on_sheet)

            custom_decks[str(deck_id_counter)] = {
                "FaceURL": face_url,
                "BackURL": back_url,
                "NumWidth": num_width,
                "NumHeight": num_height,
                "BackIsHidden": True,
                "UniqueBack": True,
                "Type": 0
            }

            cards_processed += cards_on_sheet
            deck_id_counter += 1

        # Create single combined rhythm deck
        import hashlib
        guid = hashlib.md5(f"rhythm{x}{z}".encode()).hexdigest()[:6]

        rhythm_deck = {
            "Name": "DeckCustom",
            "Transform": {
                "posX": x,
                "posY": y,
                "posZ": z,
                "rotX": 0.0,
                "rotY": 180.0,
                "rotZ": 0.0,
                "scaleX": 1.0,
                "scaleY": 1.0,
                "scaleZ": 1.0
            },
            "Nickname": "Rhythm Cards",
            "Description": "Rhythm cards for modifying gameplay",
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
            "DeckIDs": all_deck_ids,
            "CustomDeck": custom_decks,
            "LuaScript": "",
            "LuaScriptState": "",
            "XmlUI": "",
            "GUID": guid
        }
        objects.append(rhythm_deck)
        x += spacing

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

    # Stumble cards (use move card backs)
    if tts_files['stumble_fronts']:
        face_url = get_github_raw_url(username, repo, branch, tts_files['stumble_fronts'][0])
        back_url = get_github_raw_url(username, repo, branch, tts_files['move_back'])  # Use move backs

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
    print(f'  - Starter cards: {len(tts_files["starter_fronts"])} sheet(s)')
    print(f'  - Pool cards: {len(tts_files["pool_fronts"])} sheet(s)')
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
