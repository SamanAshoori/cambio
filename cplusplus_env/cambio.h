#pragma once
#include <vector>
#include <string>
#include <unordered_map>
#include "player.h"

class Cambio {
public:
    static const int RED_KING_DIAMOND = 38;
    static const int RED_KING_HEART = 51;
    static const int JOKER_1 = 52, JOKER_2 = 53;
    static const int DECK_SIZE = 54;

    Cambio();

    std::vector<int> get_deck();
    std::vector<int> get_player(int player);
    std::vector<int> get_discard_pile();
    int get_turn_count();
    bool get_game_over();
    std::string get_winner();
    std::string convert_card(int card);
    int get_card_score(int card);
    void discard(int player);
    void discard_card_from_hand(int player);
    void player_get_card_from_pile(int player);
    void player_put_card_in_hand_into_deck(int hand_index, int player);
    std::string step();
    std::vector<std::string> turn_deck_to_name(int player);
    int turn_deck_to_score(int player);

private:
    std::vector<int> deck;
    std::vector<int> discard_pile;
    Player player_one;
    Player player_two;
    int turn_count;
    bool game_over;
    int current_player_turn;
    static const std::unordered_map<int, std::string> POWER_CARDS;
};
