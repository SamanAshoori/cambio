#pragma once

#include <vector>
#include <string>

class Player{
  public:
    static const int RED_KING_DIAMOND = 38;
    static const int RED_KING_HEART = 51;

    Player(const std::vector<int>& inventory, const std::string& name);

    std::vector<int>& get_inventory();
    void set_inventory<const std::vector<int>& inventory>;
    int get_in_hand();
    void set_in_hand(int card);
    void swap_hand_with_inventory(int index);
    std::string& get_name();
    int get_score();
    int get_card_score(int card);
    int get_risk_tolerance();
    void set_risk_tolerance(int risk_tolerance);
    int decide_swap_index();

  private:
    std::vector<int> player_inventory;
    std::vector<bool> player_knowledge;
    int player_in_hand;
    std::string player_name;
    int player_score;
    int player_risk_tolerance;
    int count_of_known;

};
