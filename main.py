from cambio import Cambio


def hand_str(game, player_num):
    inv = game.get_player(player_num)
    cards = [game.convert_card(c) for c in inv]
    score = game.turn_deck_to_score(player_num)
    return f"[{', '.join(cards)}]  score={score}"


def simulate():
    game = Cambio()

    print("=" * 55)
    print("         CAMBIO - Game Simulation")
    print("=" * 55)
    print(f"P1 starting hand : {hand_str(game, 1)}")
    print(f"P2 starting hand : {hand_str(game, 2)}")
    print(f"Deck             : {len(game.get_deck())} cards")
    print()

    while True:
        if len(game.get_deck()) == 0:
            break

        turn_num = game.turn_count + 1
        player_id = game.current_player_turn
        print(f"--- Turn {turn_num} | Player {player_id} ---")

        game.step()

        print(f"  P1 : {hand_str(game, 1)}")
        print(f"  P2 : {hand_str(game, 2)}")
        print(f"  Deck: {len(game.get_deck())} cards remaining")
        print()

    print("=" * 55)
    print("GAME OVER")
    print(f"  P1 final : {hand_str(game, 1)}")
    print(f"  P2 final : {hand_str(game, 2)}")
    print(f"  Result   : {game.get_winner()}")
    print("=" * 55)


if __name__ == "__main__":
    simulate()
