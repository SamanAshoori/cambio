from player import Player
import random

deck = [i for i in range(54)]
#Cambio has 52 cards + 2 jokers (ignore for now)

random.shuffle(deck)

p = Player([deck.pop() for _ in range(4)], "Player 1")

print(p.get_card_rank(10))