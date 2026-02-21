#include "cambio.h"
#include <algorithm>
#include <random>
#include <stdexcept>
#include <iostream>

const int Cambio::RED_KING_DIAMOND;
const int Cambio::RED_KING_HEART;
const int Cambio::JOKER_1;
const int Cambio::JOKER_2;
const int Cambio::DECK_SIZE;

const std::unordered_map<int, std::string> Cambio::POWER_CARDS = {
    {6,  "PEEK_SELF"},
    {7,  "PEEK_SELF"},
    {8,  "PEEK_OPPONENT"},
    {9,  "PEEK_OPPONENT"},
    {10, "BLIND_SWAP"},
    {11, "SINGLE_PEEK_SWAP"},
    {12, "DOUBLE_PEEK_SWAP"}
};

Cambio::Cambio()
    : deck(),
      discard_pile(),
      player_one({}, "Player 1"),
      player_two({}, "Player 2"),
      turn_count(0),
      game_over(false),
      current_player_turn(1) {

    for (int i = 0; i < 54; i++) deck.push_back(i);

    std::random_device rd;
    std::mt19937 g(rd());
    std::shuffle(deck.begin(), deck.end(), g);

    std::vector<int> p1_hand, p2_hand;
    for (int i = 0; i < 4; i++) {
        p1_hand.push_back(deck.back()); deck.pop_back();
        p2_hand.push_back(deck.back()); deck.pop_back();
    }
    player_one.set_inventory(p1_hand);
    player_two.set_inventory(p2_hand);
}

// Getters
std::vector<int> Cambio::get_deck() {
    return deck;
}

std::vector<int> Cambio::get_discard_pile() {
    return discard_pile;
}

std::vector<int> Cambio::get_player(int player) {
    if (player == 1) return player_one.get_inventory();
    return player_two.get_inventory();
}

int Cambio::get_turn_count() {
    return turn_count;
}

bool Cambio::get_game_over() {
    return game_over;
}

// Logic methods
int Cambio::get_card_score(int card) {
    if (card >= 52) return 0;
    if (card == RED_KING_DIAMOND || card == RED_KING_HEART) return -1;
    int score = (card % 13) + 1;
    return score >= 10 ? 10 : score;
}

std::string Cambio::convert_card(int card) {
    if (card == -2) return "No Card";
    if (card >= 52) return "JK";
    std::string cards[] = {"A","2","3","4","5","6","7","8","9","10","J","Q","K","JK"};
    std::string suits = "SCDH";
    return cards[card % 13] + suits[card / 13];
}

void Cambio::discard(int player) {
    Player& current = (player == 1) ? player_one : player_two;
    int card = current.get_in_hand();
    if (card != -2) {
        discard_pile.push_back(card);
        current.set_in_hand(-2);
    }
}

void Cambio::discard_card_from_hand(int player) {
    Player& current = (player == 1) ? player_one : player_two;
    if (current.get_in_hand() == -2)
        throw std::runtime_error("No card in hand to discard");
    discard(player);
}

void Cambio::player_get_card_from_pile(int player) {
    Player& current = (player == 1) ? player_one : player_two;
    if (current.get_in_hand() != -2)
        throw std::runtime_error("Player already has a card in hand");
    int card = deck.back();
    deck.pop_back();
    std::cout << "Player " << player << " drew " << convert_card(card) << std::endl;
    current.set_in_hand(card);
}

void Cambio::player_put_card_in_hand_into_deck(int hand_index, int player) {
    Player& current = (player == 1) ? player_one : player_two;
    current.swap_hand_with_inventory(hand_index);
    discard(player);
}

int Cambio::turn_deck_to_score(int player) {
    std::vector<int> inv = (player == 1) ? player_one.get_inventory() : player_two.get_inventory();
    int score = 0;
    for (int card : inv) score += get_card_score(card);
    return score;
}

std::vector<std::string> Cambio::turn_deck_to_name(int player) {
    std::vector<int> inv = (player == 1) ? player_one.get_inventory() : player_two.get_inventory();
    std::vector<std::string> names;
    for (int card : inv) names.push_back(convert_card(card));
    return names;
}

std::string Cambio::get_winner() {
    int p1 = turn_deck_to_score(1);
    int p2 = turn_deck_to_score(2);
    if (p1 == p2) return "--- DRAW ---";
    else if (p1 > p2) return "--- P1 Loses ---";
    else return "--- P1 Wins ---";
}

std::string Cambio::step() {
    if (deck.empty()) {
        game_over = true;
        return get_winner();
    }

    turn_count++;
    int player_id = current_player_turn;

    player_get_card_from_pile(player_id);

    Player& current = (player_id == 1) ? player_one : player_two;
    int swap_index = current.decide_swap_index();
    if (swap_index != -1) {
        player_put_card_in_hand_into_deck(swap_index, player_id);
    }

    if (current.get_in_hand() != -2) {
        discard(player_id);
    }

    current_player_turn = (current_player_turn == 1) ? 2 : 1;

    return "";
}
