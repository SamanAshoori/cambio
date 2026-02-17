class Player:
    def __init__(self,inventory,name):
        self.player_inventory = inventory
        self.player_in_hand = -2
        self.player_name = name
        self.player_score = 0

    def get_inventory(self):
        return self.player_inventory
    
    def get_in_hand(self):
        return self.player_in_hand
    
    def get_name(self):
        return self.player_name
    
    def get_score(self):
        return self.player_score