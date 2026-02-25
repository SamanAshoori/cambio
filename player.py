class Player:
    # Define constants for special cards
    RED_KING_DIAMOND = 38
    RED_KING_HEART = 51

    POWER_CARDS = {
    "7": "PEEK_SELF", #7
    "8": "PEEK_SELF", #8
    "9": "PEEK_OPPONENT", #9
    "10": "PEEK_OPPONENT", #10
    "J": "BLIND_SWAP", #Jack
    "Q": "SINGLE_PEEK_SWAP", #Queen
    "K": "DOUBLE_PEEK_SWAP" #King
    }

    def __init__(self,inventory,name,opponent_size=4):
        self.player_inventory = inventory
        self.player_knowledge = [False for _ in inventory]
        self.player_in_hand = -2
        self.player_name = name
        self.player_score = 0
        self.risk_tolerance = 6
        self.count_of_known = sum(self.player_knowledge)
        self.opponent_size = opponent_size
        self.opponent_knowledge = [False for _ in range(opponent_size)]  # what we know about opponent
        self.opponent_inventory_known = [-1 for _ in range(opponent_size)]

    def get_inventory(self):
        return self.player_inventory
    
    def set_inventory(self, inventory):
        self.player_inventory = inventory
    
    def get_in_hand(self):
        return self.player_in_hand
    
    def set_in_hand(self, card):
        self.player_in_hand = card

    def swap_hand_with_inventory(self, index):
        temp = self.player_inventory[index]
        self.player_inventory[index] = self.player_in_hand
        self.player_in_hand = temp
        self.player_knowledge[index] = True

    def get_name(self):
        return self.player_name
    
    def get_score(self):
        return self.player_score
    
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
    
    def get_risk_tolerance(self):
        return self.risk_tolerance
    
    def set_risk_tolerance(self, risk_tolerance):
        self.risk_tolerance = risk_tolerance

    def decide_swap_index(self):
        #checks score of card in hand


        #go through all unknown cards before checking known
        hand_score = self.get_card_score(self.player_in_hand)
        if self.count_of_known < 4:
            for i, card in enumerate(self.player_inventory):
                if not self.player_knowledge[i]:
                    if hand_score < self.risk_tolerance:
                        return i

        #for loop for when we know all cards
        for i, card in enumerate(self.player_inventory):
            if self.player_knowledge[i]:
                # If we know the card, compare actual scores
                #if the card is more than the hand_card swap it at the current index[i]
                if self.get_card_score(card) > hand_score:
                    return i
        return -1
    
    def get_card_rank(self,card):
        #returns a string value for the card rank
        return ["A","2","3","4","5","6","7","8","9","10","J","Q","K","JK"][card%13]
    
    def check_if_card_is_power(self,card):
        card_rank = self.get_card_rank(card)
        if card_rank in self.POWER_CARDS:
            return True
        return False
    

