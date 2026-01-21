#Cambio
import random
from datetime import datetime

class Cambio:
    def __init__(self):
        self.deck = [i for i in range(54)]
        #Cambio has 52 cards + 2 jokers (ignore for now)

        random.shuffle(self.deck)
        #In the game of Cambio each player starts with 4 cards
        self.player_one = [self.deck.pop(),self.deck.pop(),self.deck.pop(),self.deck.pop()]
        self.player_one_in_hand = -2

        self.player_two = [self.deck.pop(),self.deck.pop(),self.deck.pop(),self.deck.pop()]
        self.player_two_in_hand = -2
        self.discard = []
    
    def get_game_details(self):
        return (self.player_one, self.player_two)
    
    def get_deck(self):
        return self.deck
    
    def set_player_one(self):
        working_deck = [21,45,52,38]
        self.player_one = working_deck
        print("player one has been set")

    def get_player_one(self):
        p1 = self.player_one
        return p1
    
    def convert_card(self,card):
        if card >= 52:
            return "JK"
        #turn the int values into a card
        cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K","JK"][card%13]
        #A = 1, JK = joker
        suits = 'SCDH'[card//13]
        # // divides and remove
        #Index 26+ is a red which means 51 = Red King  and 38 = Red King
        return cards + suits
    
    def get_card_score(self,card):
        if card >= 52:
            return 0
        #In cambio red kings are minus one so add check here
        if card == 51 | card == 38:
            return -1
        score = card % 13
        score = score + 1
        if score >= 10:
            return 10

        return score


    def turn_deck_to_name(self,player = 1):
        deck = []
        if player == 1:
            deck = self.player_one
        else:
            deck = self.player_two
        cards = []
        for card in deck:
            cards.append(self.convert_card(card))
        
        return cards
    
    def turn_deck_to_score(self, player = 1):
        deck = []
        if player == 1:
            deck = self.player_one
        else:
            deck = self.player_two
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
        

    

c = Cambio()
print(c.get_player_one())
print(c.turn_deck_to_name())
print(c.turn_deck_to_score())
print("----- PLAYER 2 SCORE BELOW -----")
print(c.turn_deck_to_name(2))
print(c.turn_deck_to_score(2))
print(c.get_winner())