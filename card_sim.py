import random
from collections import Counter
from player import Player

HAND_SIZE = 4
NUM_SIMULATIONS = 1_000_000

# Build deck excluding 10-rank cards (card%13 == 9) — those are power cards
DECK = [c for c in range(52) if c % 13 != 9]

p = Player([0, 0, 0, 0], "sim")

def score_hand(hand):
    return sum(p.get_card_score(c) for c in hand)

def run_sim():
    scores = []
    for _ in range(NUM_SIMULATIONS):
        hand = random.sample(DECK, HAND_SIZE)
        scores.append(score_hand(hand))
    return scores

def percentile(sorted_data, pct):
    idx = int(len(sorted_data) * pct / 100)
    return sorted_data[min(idx, len(sorted_data) - 1)]

if __name__ == "__main__":
    scores = run_sim()
    scores.sort()

    print(f"Simulated {NUM_SIMULATIONS:,} random {HAND_SIZE}-card hands (no 10s)\n")
    print(f"  Min score   : {scores[0]}")
    print(f"  Max score   : {scores[-1]}")
    print(f"  Mean        : {sum(scores)/len(scores):.2f}")

    for pct in [10, 20, 25, 30, 40, 50]:
        print(f"  {pct}th pct     : {percentile(scores, pct)}")

    print("\nScore distribution:")
    freq = Counter(scores)
    for score in sorted(freq):
        bar = "#" * (freq[score] * 60 // NUM_SIMULATIONS)
        print(f"  {score:3d} | {bar} ({freq[score]/NUM_SIMULATIONS*100:.1f}%)")

    print("\nCumulative % of hands at or below score:")
    running = 0
    for score in sorted(freq):
        running += freq[score]
        print(f"  <= {score:2d} : {running/NUM_SIMULATIONS*100:.1f}%")
