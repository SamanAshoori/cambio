#include "player.h"

int Player::get_score(){
  return player_score;
}

const std::vector<int>& Player::get_inventory(){
  return player_inventory;
}
