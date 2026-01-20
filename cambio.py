#Cambio
import random
from datetime import datetime

class Cambio:
    def __init__(self):
        self.deck = [i for i in range(52)]
        #Cambio has 52 cards + 2 jokers (ignore for now)

        seed = random.seed(datetime.now())
        #ramdomises seed based on time
        random.seed(seed)
        random.shuffle(self.deck)
        self.player_one = []
        self.player_two = []
    
    def get_game_details(self):
        return (self.player_one, self.player_two)
    
    def get_deck(self):
        return self.deck
    
    def set_player_one(self):
        working_deck = [0,42,12,9]
        self.player_one = working_deck
        print("player one has been set")

    def get_player_one(self):
        return self.player_one
    
    def convert_card(card):
        #turn the int values into a card
        cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K","JK"][card%13]
        #A = 1, JK = joker
        suits = 'SCDH'[card//13]
        # // divides and remove
        #Index 26+ is a red which means 51 = Red King  and 38 = Red King
        return cards + suits
    
    def convert_all_cards(self):
        cards = []
        for card in self.player_one:
            print(self.convert_card(card))
            cards.append(self.convert_card(card))
        
        return cards

    

c = Cambio
c.set_player_one(c)
print(c.get_player_one(c))
print(c.convert_all_cards(c))