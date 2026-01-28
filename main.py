from cambio import Cambio

c = Cambio()
print("----- INITIAL GAME STATE -----")
print("Deck size:", len(c.get_deck()))
print(c.turn_deck_to_name())
print(c.turn_deck_to_score())
print(c.get_discard_pile())

print("----- PLAYER 2 SCORE BELOW -----")
print(c.turn_deck_to_name(2))
print(c.turn_deck_to_score(2))
print("----- SIMULATING TURNS -----")
for i in range(10):
    c.step()
    print(f"--- TURN {i+1} ---")
    print("Deck size:", len(c.get_deck()))
    print("Discard pile size:", len(c.discard))
    print("Dicarded cards:", [c.convert_card(card) for card in c.discard])
    print(f"Cards in hand P1: {c.get_card_score(c.player_one_in_hand)}, P2: {c.get_card_score(c.player_two_in_hand)}")
    print("P1:",c.turn_deck_to_name(), "SCORE:", c.turn_deck_to_score())
    print("P2:",c.turn_deck_to_name(2), "SCORE:", c.turn_deck_to_score(2))
print("----- GAME OVER -----")
print(c.get_winner())