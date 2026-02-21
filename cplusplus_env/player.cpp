#include "player.h"

int Player::get_score(){
  return player_score;
}

std::vector<int>& Player::get_inventory(){
  return player_inventory;
}

void Player::set_inventory(const std::vector<int>& inventory){
  player_inventory = inventory;
}

int Player::get_in_hand(){
  return player_in_hand;
}

void Player::set_in_hand(int card){
  player_in_hand = card;
}

std::string& Player::get_name(){
  return player_name;
}

int Player::get_risk_tolerance(){
  return player_risk_tolerance;
}

void Player::set_risk_tolerance(int risk_tolerance){
  player_risk_tolerance = risk_tolerance;
}
