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


def create_deck_object(name, face_url, back_url, num_cards, position, description=""):
    """Create a TTS deck object with proper configuration"""

    # Generate unique GUID for this deck
    import hashlib
    guid = hashlib.md5(f"{name}{position[0]}{position[2]}".encode()).hexdigest()[:6]

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
        "DeckIDs": list(range(100, 100 + num_cards)),
        "CustomDeck": {
            "1": {
                "FaceURL": face_url,
                "BackURL": back_url,
                "NumWidth": 10,
                "NumHeight": 7,
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


def generate_tts_save(username, repo, tts_files, branch="main"):
    """Generate complete TTS save file JSON"""

    objects = []

    # Starting position for first deck
    x, y, z = 0, 1, 0
    spacing = 4  # Space between decks

    # Move card decks (can be multiple sheets)
    for i, front_file in enumerate(tts_files['move_fronts'], 1):
        # Calculate number of cards (70 for full sheets, less for last sheet)
        num_cards = 70  # Assume 70, TTS will handle if less

        face_url = get_github_raw_url(username, repo, branch, front_file)
        back_url = get_github_raw_url(username, repo, branch, tts_files['move_back'])

        deck = create_deck_object(
            name=f"Move Cards {i}" if len(tts_files['move_fronts']) > 1 else "Move Cards",
            face_url=face_url,
            back_url=back_url,
            num_cards=num_cards,
            position=[x, y, z],
            description=f"Dance move cards - Sheet {i}"
        )
        objects.append(deck)
        x += spacing

    # Rhythm card decks
    for i, front_file in enumerate(tts_files['rhythm_fronts'], 1):
        face_url = get_github_raw_url(username, repo, branch, front_file)
        back_url = get_github_raw_url(username, repo, branch, tts_files['rhythm_back'])

        deck = create_deck_object(
            name=f"Rhythm Cards {i}" if len(tts_files['rhythm_fronts']) > 1 else "Rhythm Cards",
            face_url=face_url,
            back_url=back_url,
            num_cards=70,
            position=[x, y, z],
            description=f"Rhythm cards - Sheet {i}"
        )
        objects.append(deck)
        x += spacing

    # Judge cards
    if tts_files['judge_fronts']:
        face_url = get_github_raw_url(username, repo, branch, tts_files['judge_fronts'][0])
        back_url = get_github_raw_url(username, repo, branch, tts_files['judge_back'])

        deck = create_deck_object(
            name="Judge Cards",
            face_url=face_url,
            back_url=back_url,
            num_cards=12,  # Actual count
            position=[x, y, z],
            description="Judge cards with special requirements"
        )
        objects.append(deck)
        x += spacing

    # Stumble cards
    if tts_files['stumble_fronts']:
        face_url = get_github_raw_url(username, repo, branch, tts_files['stumble_fronts'][0])
        back_url = get_github_raw_url(username, repo, branch, tts_files['stumble_back'])

        deck = create_deck_object(
            name="Stumble Cards",
            face_url=face_url,
            back_url=back_url,
            num_cards=20,  # Actual count
            position=[x, y, z],
            description="Stumble penalty cards"
        )
        objects.append(deck)

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
