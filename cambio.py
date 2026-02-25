#Cambio env
import random
from player import Player


class Cambio:
    # Define constants for special cards
    RED_KING_DIAMOND = 38
    RED_KING_HEART = 51
    JOKER_1 = 52
    JOKER_2 = 53
    DECK_SIZE = 54

    #Powercards Dict
    POWER_CARDS = {
        6: "PEEK_SELF", #7
        7: "PEEK_SELF", #8
        8: "PEEK_OPPONENT", #9
        9: "PEEK_OPPONENT", #10
        10: "BLIND_SWAP", #Jack
        11: "SINGLE_PEEK_SWAP", #Queen
        12: "DOUBLE_PEEK_SWAP" #King
        }
        

    def __init__(self):
        self.deck = [i for i in range(54)]
        #Cambio has 52 cards + 2 jokers (ignore for now)

        random.shuffle(self.deck)
        #In the game of Cambio each player starts with 4 cards
        self.player_one = Player([self.deck.pop() for _ in range(4)], "Player 1")
        self.player_two = Player([self.deck.pop() for _ in range(4)], "Player 2")

        self.discard_pile = []
        self.turn_count = 0
        self.game_over = False
        self.current_player_turn = 1
    
    def get_game_details(self):
        return (self.player_one.get_inventory(), self.player_two.get_inventory())

    def get_deck(self):
        return self.deck

    def get_player(self, player = 1):
        if player == 1:
            return self.player_one.get_inventory()
        else:
            return self.player_two.get_inventory()

    def convert_card(self,card):
        #check for -2
        if card == -2:
            return "No Card"
        #check for joker
        if card >= 52:
            return "JK"
        #turn the int values into a card
        cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K","JK"][card%13]
        #A = 1, JK = joker
        #// MEANS DIVIDE AND FLOOR (FLOOR REMOVES DECIMALS)
        suits = 'SCDH'[card//13]
        return cards + suits
    
    def get_card_score(self,card):
        if card >= 52:
            return 0
        #In cambio red kings are minus one so add check here
        if card == self.RED_KING_DIAMOND or card == self.RED_KING_HEART:
            #red kings are worth -1
            return -1
        score = card % 13
        score = score + 1
        if score >= 10:
            return 10

        return score
    
    def discard(self,player = 1):
        current_player = self.player_one if player == 1 else self.player_two
        card = current_player.get_in_hand()
        if card != -2:
            self.discard_pile.append(card)
            current_player.set_in_hand(-2)
    
    def player_put_card_in_hand_into_deck(self, hand_index, player = 1):
        current_player = self.player_one if player == 1 else self.player_two
        current_player.swap_hand_with_inventory(hand_index)
        self.discard(player)
    
    def discard_card_from_hand(self, player = 1):
        current_player = self.player_one if player == 1 else self.player_two
        if current_player.get_in_hand() == -2:
            raise Exception("No card in hand to discard")
        self.discard(player)

    def player_get_card_from_pile(self,player = 1):
        current_player = self.player_one if player == 1 else self.player_two
        #quick check to see if player has a card in hand already
        if current_player.get_in_hand() != -2:
            raise Exception(f"Player {player} already has a card in hand")
        card = self.deck.pop()
        print(f"Player {player} drew {self.convert_card(card)}")
        current_player.set_in_hand(card)

    def step(self):

        if len(self.deck) == 0:  
            self.game_over = True
            return self.get_winner()
        else:
            #simulate one turn of the game
            self.turn_count += 1
            
            current_player = self.player_one if self.current_player_turn == 1 else self.player_two
            player_id = self.current_player_turn

            # Player draws a card
            self.player_get_card_from_pile(player_id)

            # Player decides what to do (Swap or Stick)
            swap_index = current_player.decide_swap_index()
            if swap_index != -1:
                self.player_put_card_in_hand_into_deck(swap_index, player_id)

            # Discard if they still have a card in hand
            if current_player.get_in_hand() != -2:
                self.discard(player_id)

            self.current_player_turn = 2 if self.current_player_turn == 1 else 1
            
    def get_card_rank(self,card):
        #returns a string value for the card rank
        return ["A","2","3","4","5","6","7","8","9","10","J","Q","K","JK"][card%13]


    def turn_deck_to_name(self,player = 1):
        deck = self.player_one.get_inventory() if player == 1 else self.player_two.get_inventory()
        cards = []
        for card in deck:
            cards.append(self.convert_card(card))
        
        return cards
    
    def turn_deck_to_score(self, player = 1):
        deck = self.player_one.get_inventory() if player == 1 else self.player_two.get_inventory()
        score = 0
        for card in deck:
            #checks each card in the player one deck and turns it into a value
            score += self.get_card_score(card)
        
        return score
    
    
    def get_winner(self):
        p1_score = self.turn_deck_to_score()
        p2_score = self.turn_deck_to_score(2)

        if p1_score == p2_score:
            return "--- DRAW ---"
        elif p1_score > p2_score:
            return "--- P1 Loses ---"
        else:
            return "--- P1 Wins ---"
        
    def get_discard_pile(self):
        return self.discard_pile
