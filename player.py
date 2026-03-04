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
        self.opponent_inventory = [-1 for _ in range(opponent_size)]

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
        self.count_of_known = sum(self.player_knowledge)

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
        hand_score = self.get_card_score(self.player_in_hand)

        # First: swap a known card that's worse than what we're holding
        for i, card in enumerate(self.player_inventory):
            if self.player_knowledge[i]:
                if self.get_card_score(card) > hand_score:
                    return i

        # Second: blindly swap into an unknown slot if hand score is below risk tolerance
        for i in range(len(self.player_inventory)):
            if not self.player_knowledge[i]:
                if hand_score < self.risk_tolerance:
                    return i

        return -1
    
    def get_card_rank(self,card):
        #returns a string value for the card rank
        return ["A","2","3","4","5","6","7","8","9","10","J","Q","K","JK"][card%13]
    
    def get_average_known_card_score(self):
        total = 0
        for i,known in enumerate(self.player_knowledge):
            if known:
                total += self.get_card_score(self.player_inventory[i])
        if self.count_of_known == 0:
            return 0
        return total / self.count_of_known
    
    def risk_tolerance_calc(self):
        new_risk_tolerance = 0
        unknown_score = (len(self.player_inventory) - self.count_of_known) * 6
        total = 0
        for i, known in enumerate(self.player_knowledge):
            if known:
                total += self.get_card_score(self.player_inventory[i])
        new_risk_tolerance += ((unknown_score + total) / len(self.player_inventory))
        return new_risk_tolerance
        
    
    def set_risk_tolerance(self):
        self.risk_tolerance = self.risk_tolerance_calc()

    
    def check_if_card_is_power(self,card):
        card_rank = self.get_card_rank(card)
        if card_rank in self.POWER_CARDS:
            return True
        return False
    
    def check_if_peek_self(self,card):
        card_rank = self.get_card_rank(card)
        return self.POWER_CARDS.get(card_rank) == "PEEK_SELF"
    
    def check_if_peek_opponent(self,card):
        card_rank = self.get_card_rank(card)
        return self.POWER_CARDS.get(card_rank) == "PEEK_OPPONENT"

    def check_if_blind_swap(self,card):
        card_rank = self.get_card_rank(card)
        return self.POWER_CARDS.get(card_rank) == "BLIND_SWAP"

    def check_if_single_peek_swap(self,card):
        card_rank = self.get_card_rank(card)
        return self.POWER_CARDS.get(card_rank) == "SINGLE_PEEK_SWAP"

    def check_if_double_peek_swap(self,card):
        card_rank = self.get_card_rank(card)
        return self.POWER_CARDS.get(card_rank) == "DOUBLE_PEEK_SWAP"
    
    def peek_self(self, index=None):
        if index is None:
            for i, known in enumerate(self.player_knowledge):
                if not known:
                    index = i
                    break
        if index is None:
            return -1
        self.player_knowledge[index] = True
        self.count_of_known = sum(self.player_knowledge)
        return index

    def peek_opponent(self, opponent_inventory, index=None):
        if index is None:
            for i, known in enumerate(self.opponent_knowledge):
                if not known:
                    index = i
                    break
        if index is None:
            return -1
        self.opponent_knowledge[index] = True
        self.opponent_inventory_known[index] = opponent_inventory[index]
        return index
        
    def get_highest_known_card_index(self):
        known_indices = [i for i, known in enumerate(self.player_knowledge) if known]
        if not known_indices:
            return -1
        return max(known_indices, key=lambda i: self.get_card_score(self.player_inventory[i]))
    
    def get_highest_opponent_known_card_index(self):
        known_indices = [i for i, known in enumerate(self.opponent_knowledge) if known]
        if not known_indices:
            return -1
        return max(known_indices, key=lambda i: self.get_card_score(self.opponent_inventory[i]))
    
    def decide_blind_swap(self):
        own_index = self.get_highest_known_card_index()

        # No known own cards — can't make an informed decision
        if own_index == -1:
            return (-1, -1)

        own_score = self.get_card_score(self.player_inventory[own_index])

        # Our worst known card is below risk tolerance — not worth offloading
        if own_score < self.risk_tolerance:
            return (-1, -1)

        known_opp = [i for i, known in enumerate(self.opponent_knowledge) if known]
        if known_opp:
            # Pick opponent's lowest scoring known card (best card for us to receive)
            opponent_index = min(known_opp, key=lambda i: self.get_card_score(self.opponent_inventory[i]))
            opp_score = self.get_card_score(self.opponent_inventory[opponent_index])
            # Only swap if we actually gain (their card scores lower than our worst)
            if opp_score >= own_score:
                return (-1, -1)
        else:
            # Truly blind — pick opponent slot 0
            opponent_index = 0

        return (own_index, opponent_index)
    
