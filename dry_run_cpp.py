from cambio_cpp import Cambio as CambioCpp

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
for i in range(20):
    c.step()
    print(f"--- TURN {i+1} ---")
    print("Deck size:", len(c.get_deck()))
    print("Discard pile size:", len(c.discard_pile))
    print("Discarded cards:", [c.convert_card(card) for card in c.discard_pile])
    print(f"Cards in hand P1: {c.convert_card(c.player_one.get_in_hand())}, P2: {c.convert_card(c.player_two.get_in_hand())}")
    print("P1:",c.turn_deck_to_name(), "SCORE:", c.turn_deck_to_score())
    print("P2:",c.turn_deck_to_name(2), "SCORE:", c.turn_deck_to_score(2))
print("----- GAME OVER -----")
print(c.get_winner())
