from cambio import Cambio

# ANSI colours
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"
RED     = "\033[91m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[94m"
MAGENTA = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"

POWER_COLOUR = {
    "PEEK_SELF":          CYAN,
    "PEEK_OPPONENT":      MAGENTA,
    "BLIND_SWAP":         YELLOW,
    "SINGLE_PEEK_SWAP":   GREEN,
    "DOUBLE_PEEK_SWAP":   RED,
}

POWER_ICON = {
    "PEEK_SELF":          "👁  PEEK SELF",
    "PEEK_OPPONENT":      "🔍 PEEK OPPONENT",
    "BLIND_SWAP":         "🔀 BLIND SWAP",
    "SINGLE_PEEK_SWAP":   "↔  SINGLE PEEK SWAP",
    "DOUBLE_PEEK_SWAP":   "↔↔ DOUBLE PEEK SWAP",
}


def hand_known(game, player_obj, player_num):
    """Show hand using the player's own knowledge — unknown slots shown as ??"""
    inv       = player_obj.player_inventory
    knowledge = player_obj.player_knowledge
    parts = []
    for i, card in enumerate(inv):
        if knowledge[i]:
            parts.append(f"{GREEN}{game.convert_card(card)}{RESET}")
        else:
            parts.append(f"{DIM}??{RESET}")
    actual = game.turn_deck_to_score(player_num)
    return f"[{', '.join(parts)}]  {DIM}(actual score: {actual}){RESET}"


def hand_actual(game, player_num):
    """Reveal all cards — used at game over."""
    inv   = game.get_player(player_num)
    score = game.turn_deck_to_score(player_num)
    cards = [f"{WHITE}{game.convert_card(c)}{RESET}" for c in inv]
    return f"[{', '.join(cards)}]  score={BOLD}{score}{RESET}"


def opp_knowledge(game, player_obj):
    """What this player knows about the opponent."""
    parts = []
    for i, known in enumerate(player_obj.opponent_knowledge):
        if known:
            parts.append(f"{MAGENTA}{game.convert_card(player_obj.opponent_inventory[i])}{RESET}")
        else:
            parts.append(f"{DIM}??{RESET}")
    return f"[{', '.join(parts)}]"


def print_state(game):
    p1 = game.player_one
    p2 = game.player_two
    print(f"  {BOLD}P1{RESET}  hand      : {hand_known(game, p1, 1)}")
    print(f"      knows opp : {opp_knowledge(game, p1)}")
    print(f"  {BOLD}P2{RESET}  hand      : {hand_known(game, p2, 2)}")
    print(f"      knows opp : {opp_knowledge(game, p2)}")
    print(f"  {DIM}Deck: {len(game.get_deck())} cards remaining{RESET}")


def simulate():
    game = Cambio()
    game.starting_peek()

    print(f"\n{BOLD}{'═' * 52}{RESET}")
    print(f"{BOLD}{'CAMBIO  —  Game Simulation':^52}{RESET}")
    print(f"{BOLD}{'═' * 52}{RESET}\n")
    print(f"  {CYAN}Starting peek done — each player knows their first 2 cards{RESET}\n")
    print_state(game)
    print()

    while True:
        if len(game.get_deck()) == 0:
            break

        turn_num  = game.turn_count + 1
        player_id = game.current_player_turn

        print(f"{BOLD}{'─' * 52}{RESET}")
        print(f"{BOLD}  Turn {turn_num}  |  Player {player_id}{RESET}")
        print(f"{'─' * 52}")

        game.step()

        drawn = getattr(game, 'last_drawn', None)
        power = getattr(game, 'last_power', None)

        if drawn is not None:
            card_name = game.convert_card(drawn)
            if power:
                col  = POWER_COLOUR.get(power, YELLOW)
                icon = POWER_ICON.get(power, power)
                print(f"  Drew : {BOLD}{card_name}{RESET}  →  {col}{BOLD}{icon}{RESET}")
            else:
                print(f"  Drew : {BOLD}{card_name}{RESET}")

        print()
        print_state(game)
        print()

    print(f"\n{BOLD}{'═' * 52}{RESET}")
    print(f"{BOLD}{'G A M E   O V E R':^52}{RESET}")
    print(f"{'═' * 52}{RESET}")
    print(f"  P1 : {hand_actual(game, 1)}")
    print(f"  P2 : {hand_actual(game, 2)}")
    result = game.get_winner()
    print(f"\n  {BOLD}{YELLOW}{result:^52}{RESET}")
    print(f"{BOLD}{'═' * 52}{RESET}\n")


if __name__ == "__main__":
    simulate()
