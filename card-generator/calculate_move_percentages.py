#!/usr/bin/env python3
"""
Calculate percentages of move types in the pool deck
This is used to add helpful statistics to rhythm cards
"""

import csv
from pathlib import Path
from collections import Counter

def calculate_move_percentages():
    """Calculate percentage of each move type in pool deck"""
    base_dir = Path(__file__).parent.parent
    moves_csv = base_dir / 'card-data' / 'moves.csv'

    # Count move types in pool deck only
    type_counts = Counter()
    total_pool_moves = 0

    with open(moves_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['deck_type'] == 'pool':
                move_type = row['type']
                type_counts[move_type] += 1
                total_pool_moves += 1

    # Calculate percentages
    percentages = {}
    for move_type, count in type_counts.items():
        percentage = round((count / total_pool_moves) * 100)
        percentages[move_type] = percentage

    return percentages, total_pool_moves

if __name__ == '__main__':
    percentages, total = calculate_move_percentages()

    print('Move Type Distribution in Pool Deck:')
    print(f'Total pool moves: {total}')
    print()

    for move_type, percent in sorted(percentages.items()):
        count = round((percent / 100) * total)
        print(f'{move_type:8} {count:3} cards ({percent:2}%)')
