#include "player.h"

Player::Player(const std::vector<int>& inventory, const std::string& name)
    : player_inventory(inventory),
      player_name(name),
      player_knowledge(inventory.size(), false),
      player_in_hand(-2),
      player_score(0),
      player_risk_tolerance(6),
      count_of_known(0) {
}

const int Player::RED_KING_DIAMOND;
const int Player::RED_KING_HEART;

int Player::get_score(){
  return player_score;
}

const std::vector<int>& Player::get_inventory(){
  return player_inventory;
}

void Player::set_inventory(const std::vector<int>& inventory) {
    player_inventory = inventory;
    player_knowledge.assign(inventory.size(), false);
}
int Player::get_in_hand(){
  return player_in_hand;
}

void Player::set_in_hand(int card){
  player_in_hand = card;
}

const std::string& Player::get_name(){
  return player_name;
}

int Player::get_risk_tolerance(){
  return player_risk_tolerance;
}

void Player::set_risk_tolerance(int risk_tolerance){
  player_risk_tolerance = risk_tolerance;
}

int Player::get_card_score(int card){
  int score = 0;
  if (card >= 52){
    return 0;
    //this is because jokers are above 52
  }
  if ((card == RED_KING_DIAMOND) || (card == RED_KING_HEART)){
    return -1;
  }
  score = card % 13;
  score = score + 1;
  if (score >= 10){
    return 10;
  }
  return score;
}

int Player::decide_swap_index(){
  int hand_score = get_card_score(player_in_hand);
  if(count_of_known < 4){
    for(int i = 0; i < player_inventory.size();i++){
      if(!player_knowledge[i]){
        if(hand_score < player_risk_tolerance){
          return i;
        }
      }
    }
  }
  //for loop for when when we kow all the cards in inventory
  for(int i = 0;i <player_inventory.size();i++){
    if(player_knowledge[i]){
      if(get_card_score(player_inventory[i]) > hand_score){
        return i; 
      }
    }
  }
  //if all fails then return -1
  return -1;

}

void Player::swap_hand_with_inventory(int index){
  int temp = player_inventory[index];
  player_inventory[index] = player_in_hand;
  player_in_hand = temp;
  player_knowledge[index] = true;

}
