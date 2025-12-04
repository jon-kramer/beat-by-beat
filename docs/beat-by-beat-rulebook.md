# Beat by Beat

*A Dance-Themed Deck Builder*

---

## Game Overview

Beat by Beat is a competitive deck-building game for 2–4 players where you choreograph dance routines, chain together moves, and compete for crowd favor. Each player builds and refines a personal deck of dance moves over the course of six rounds, aiming to impress both the crowd and a panel of judges.

A game consists of **6 rounds** (called *phrases*). Each phrase contains **8 beats** (turns). At the end of the game, the player with the highest score wins.

---

## Components

### Move Cards

Move cards are the core of the game. Each move card has the following attributes:

- **Execution Cost** — A number (1–5) indicating how difficult the move is to perform.
- **Style** — The dance style: Latin, Ballroom, Classical, Jazz, or Street.
- **Type** — A movement category: Step, Spin, Jump, Pose, Flow, or Pop.
- **Bonus Score** (some cards) — Points awarded at the end of the round if successfully executed.

### Move Types

| Type | Description |
|------|-------------|
| Step | Grounded footwork and traveling patterns |
| Spin | Rotations and turns |
| Jump | Aerial moves, leaving the ground |
| Pose | Held positions and shapes |
| Flow | Continuous, wave-like movement |
| Pop | Sharp, staccato, isolated hits |

### Starter Deck Cards

Each player begins with a 10-card starter deck of styleless basic moves. These cards have no Style and cannot satisfy Judge style requirements.

### Stumble Cards

Stumble cards represent a failed performance. They have an Execution Cost of 0, no Style, no Type, no Bonus Score, cannot win crowd favor, and provide no discount to subsequent moves. Players are forced to take a Stumble when they have no cards in hand. Stumble cards remain in your deck permanently unless removed via Refinement.

### Rhythm Cards

Rhythm cards modify individual beats. The Rhythm deck contains 80 cards—approximately 60% have no effect (with flavor text), while the remainder provide bonuses such as reducing execution costs, increasing bonus scores, granting bonus recovery actions, or modifying crowd favor rules. Some effects are conditional based on a move's Style or Type.

### Judge Cards

Judge cards provide an alternate scoring path. Each Judge has a requirement (e.g., "5 Latin + 3 Any successfully executed"). If a player meets a Judge's criteria across all 8 beats of a round, they claim that Judge permanently and receive an immediate point reward plus an ongoing benefit.

### Common Move Pool

A shared deck of move cards that all players draft from via the Inspiration recovery action. Cards rejected during drafts go to a common discard pile, which reshuffles into the pool when needed.

---

## Game Setup

1. **Prepare Rhythm Cards:** Shuffle the 80-card Rhythm deck. Deal 8 cards face-up in a row (Round 1). Deal 8 cards face-down below them (Round 2—to be revealed at end of Round 1). Remaining cards form the Rhythm draw pile.

2. **Set Out Judge Cards:** Shuffle the 12 Judge cards. Deal face-up: 3 Judges (2 players), 4 Judges (3 players), or 5 Judges (4 players). Return unused Judges to the box unseen.

3. **Prepare Common Move Pool:** Shuffle the Common Move Pool deck (120 cards: 100 styled + 20 multi-style) and place it within reach of all players. Set aside space for the common discard pile.

4. **Distribute Starter Decks:** Give each player their 10-card starter deck of styleless basic moves.

5. **Initial Draft:** Each player draws 5 cards from the Common Move Pool, selects 3 to add to their deck, and places the remaining 2 in the common discard pile (face-down). This draft occurs after players can see the Round 1 and Round 2 Rhythm cards and Judges.

6. **Draw Starting Hands:** Each player shuffles their deck (now 13 cards) and draws 5 cards.

---

## Round Structure

Each round (phrase) consists of 8 beats played in sequence. After completing all 8 beats, perform end-of-round scoring and reset for the next round.

### Beat Flow

Each beat proceeds through these phases:

1. **Select:** All players simultaneously choose a move card from their hand and place it face-down. If a player's hand is empty, they must take a Stumble card and play that instead.

2. **Reveal:** All players flip their cards face-up.

3. **Execute:** Resolve each move's execution (see Execution below).

4. **Crowd Favor:** Determine which move(s) win crowd favor (see Crowd Favor below).

5. **Recovery:** Each player selects one recovery action, plus any bonus actions earned (see Recovery Actions below).

---

## Execution

To execute a move, you must pay its **Execution Cost** by discarding cards from your hand equal to (Cost − 1). A cost-1 move requires no discards; a cost-3 move requires discarding 2 cards.

### Discounts

The effective cost of a move can be reduced by:

- **Chaining:** If your previous beat's move was successfully executed AND its cost is less than or equal to your current move's cost, you receive a discount equal to the previous move's cost.
- **Crowd Favor Bonus:** If your previous move won crowd favor (outright, not style-matched), you receive an additional +1 discount.
- **Rhythm Card Effects:** The active Rhythm card for this beat may provide cost reductions.

**Important:** If a move's cost drops to 0 or below after discounts, no cards need to be discarded.

### Mandatory Payment

If you have enough cards in hand to pay the (discounted) cost, you **must** pay it. You cannot voluntarily fail a move.

### Failed Execution

If you cannot pay the cost, the move fails. Flip the card face-down to indicate failure. Failed moves do not provide chaining discounts, cannot win crowd favor, and do not count toward Judge requirements.

### Execution Example

*The following example shows how chaining works across a full phrase:*

| Beat | Cost | Discount | Discards | Notes |
|------|------|----------|----------|-------|
| 1 | 1 | — | 0 | Cost 1 needs 0 discards |
| 2 | 2 | 1 (from Beat 1) | 0 | Effective cost = 1 |
| 3 | 4 | 2 (from Beat 2) | 1 | Effective cost = 2 |
| 4 | 4 | 4 (from Beat 3) | 0 | Effective cost = 0 |
| 5 | 3 | 0 (cost dropped) | 2 | No chain discount |
| 6 | 5 | 3 (from Beat 5) | 1 | Needs 1 card; fails if 0 in hand |
| 7 | 5 | 0 (Beat 6 failed) | 4 | No discount from failed move |
| 8 | 2 | 0 (Beat 7 failed) | 1 | Recovers the chain |

---

## Crowd Favor

After execution, determine which moves win crowd favor for this beat.

### Winning Crowd Favor

A move wins crowd favor if:

- It was successfully executed, AND
- Its Execution Cost is strictly higher than all other successfully executed moves this beat.

**Ties:** If multiple players tie for the highest cost, none of them win crowd favor.

**Style Matching:** If another player's successfully executed move shares the same Style as a winning move, that player also "wins" crowd favor for scoring purposes. Rotate both cards sideways to indicate this.

### Crowd Favor Rewards

- **Next-Beat Discount:** Only the player who won outright (highest cost) receives a +1 discount on their next beat. Style-matchers do not receive this bonus.
- **End-of-Round Scoring:** Both outright winners and style-matchers count their wins toward end-of-round placement scoring (see Scoring).

---

## Recovery Actions

After crowd favor is resolved, each player chooses **one** recovery action. Players may also take any bonus recovery actions granted by Rhythm cards, move effects, or other sources.

**Actions resolve in this order:** Stamina → Refinement → Inspiration

1. **Stamina:** Draw 2 cards from your personal deck.

2. **Refinement:** Take a card from your hand or personal discard pile and place it face-down in the common discard pile. (This removes the card from your deck permanently.)

3. **Inspiration:** Draw 3 cards from the Common Move Pool. Choose 2 to add to your personal discard pile (face-down). Place the remaining 1 in the common discard pile (face-down).

**Inspiration Shortage:** If multiple players choose Inspiration but there aren't enough cards in the Common Move Pool, first reshuffle the common discard pile into the pool. If there still aren't enough cards, none of the Inspiration actions resolve.

### Deck Cycling

When your personal draw deck is empty and you need to draw, shuffle your personal discard pile to form a new deck.

---

## End of Round

After beat 8 of each round:

1. **Score Move Bonuses:** Total the Bonus Score values on all successfully executed moves this round.

2. **Score Crowd Favor Placement:** Rank players by number of crowd favor wins (including style-matches). Award 8 points for 1st place, 4 for 2nd, 2 for 3rd. Split points for ties (e.g., two players tied for 1st split 12 points for 6 each).

3. **Award Judges:** If any player met a Judge's requirements this round, they claim that Judge permanently, receive its point reward, and gain its ongoing benefit.

4. **Advance Rhythm Cards:** Remove the current round's Rhythm cards to a discard pile. Flip the next round's cards face-up. Deal 8 new cards face-down from the Rhythm draw pile (these become the round after next, maintaining one-round-ahead visibility). Skip this step after Round 5.

5. **Reset for Next Round:** Each player shuffles their hand and personal discard pile back into their deck, then draws 5 cards.

---

## Scoring and Winning

Players accumulate points throughout the game from:

1. **Move Bonus Scores:** Summed at the end of each round for successfully executed moves.

2. **Crowd Favor Placement:** 8 / 4 / 2 points for 1st / 2nd / 3rd place each round.

3. **Judge Rewards:** Immediate points from claimed Judges, plus any ongoing point bonuses.

After 6 rounds, the player with the highest total score wins.

**Tiebreaker:** If tied, the player with fewer cards in their deck wins.

---

## Rhythm Card Visibility

Players can always see:
- The current round's 8 Rhythm cards
- The next round's 8 Rhythm cards

This allows tactical planning for the current round and strategic drafting for the next.

---

## Multi-Style Cards

Some move cards belong to two styles (e.g., "Latin / Ballroom"). When playing a multi-style card:

- For **Judge requirements:** The card counts as ONE of its listed styles (player's choice when claiming).
- For **Style matching:** The card can match with either of its styles for crowd favor purposes.
- For **Ongoing effects:** Multi-style cards do not benefit from style-specific bonuses (e.g., "+1 bonus to Latin moves") unless otherwise specified.

---

## Experimental Rules

*The following ideas are under consideration and not part of the core rules:*

- **Move Bonus Effects:** Individual move cards may have unique triggered abilities when successfully executed.

- **Crowd Favor Tokens:** Winning crowd favor awards tokens that provide permanent execution cost discounts.

- **Bonus Recovery on Crowd Favor:** Winning crowd favor grants an extra recovery action that beat.

- **Variable Crowd Bonuses:** Each round has unique crowd-related bonuses to compete for.

- **Judge Drafting:** Before the game, each player drafts one Judge as "their" Judge to pursue, receiving +2 bonus points if they claim it.

---

## Quick Reference

### Beat Sequence

Select → Reveal → Execute → Crowd Favor → Recovery

### Execution Cost Formula

Discards Required = Cost − 1 − Discounts

### Chaining Discount

If previous move succeeded AND previous cost ≤ current cost → Discount = previous cost

### Recovery Actions

- Stamina: Draw 2 from personal deck
- Refinement: Remove 1 card from hand or discard
- Inspiration: Draw 3 from Pool, keep 2, discard 1

### Crowd Favor Scoring

1st: 8 pts | 2nd: 4 pts | 3rd: 2 pts (split ties)

### Game Length

6 rounds × 8 beats = 48 total beats

### Component Summary

| Component | Count |
|-----------|-------|
| Starter Deck (per player) | 10 cards |
| Common Move Pool | 120 cards |
| Rhythm Deck | 80 cards |
| Judge Cards | 12 cards |
| Stumble Cards | ~20 cards |

---

*Version 2.0 — Updated with refined Inspiration, Rhythm visibility, and Type system*
