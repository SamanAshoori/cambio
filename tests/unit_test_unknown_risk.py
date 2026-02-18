import unittest
import sys
import os

# Add the parent directory to sys.path to allow importing from the sibling directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from player import Player

class TestPlayerRiskLogic(unittest.TestCase):
    def setUp(self):
        # Cards: 10 (Jack, score 10), 4 (5, score 5), 11 (Queen, score 10), 1 (2, score 2)
        self.inventory = [10, 4, 11, 1] 
        self.player = Player(self.inventory, "Test Player")
        self.player.player_knowledge = [False, False, False, False]
        self.player.set_risk_tolerance(6)

    def test_unknown_card_high_hand_value(self):
        """Hand score (10) >= risk (6) with unknown inventory: No swap."""
        self.player.set_in_hand(12) # King of Spades (Score 10)
        print("Card in Hand is a 10 and we have now knowledge and risk factor is 6 ")
        print(self.player.decide_swap_index())
        self.assertEqual(self.player.decide_swap_index(), -1)

    def test_unknown_card_high_hand_value_rf10(self):
        self.player.set_risk_tolerance(10)

        """Hand score (10) >= risk (6) with unknown inventory: No swap."""
        self.player.set_in_hand(12) # King of Spades (Score 10)
        print("Card in Hand is a 10 and we have now knowledge and risk factor is 10 ")
        print(self.player.decide_swap_index())
        self.assertEqual(self.player.decide_swap_index(), -1)
    
    def test_unknown_card_high_hand_value_rf12(self):
        self.player.set_risk_tolerance(12)

        """Hand score (10) >= risk (6) with unknown inventory: swap."""
        self.player.set_in_hand(12) # King of Spades (Score 10)
        print("Card in Hand is a 10 and we have now knowledge and risk factor is 12 ")
        print(self.player.decide_swap_index())
        self.assertEqual(self.player.decide_swap_index(), 0)

    def test_unknown_card_low_hand_value(self):
        """Hand score (3) < risk (6) with unknown inventory: Swap at index 0."""
        self.player.set_in_hand(2) # 3 of Spades (Score 3)
        self.assertEqual(self.player.decide_swap_index(), 0)

    def test_known_card_logic(self):
        """Known inventory (10) > hand (5): Swap at index 0."""
        self.player.player_knowledge[0] = True
        self.player.set_in_hand(4) 
        self.assertEqual(self.player.decide_swap_index(), 0)

    def test_skip_known_bad_swap_for_unknown_risk(self):
        """Skip known bad swap at index 0, take risk at index 1."""
        self.player.player_inventory[0] = 1 
        self.player.player_knowledge[0] = True 
        self.player.set_in_hand(4)
        self.assertEqual(self.player.decide_swap_index(), 1)

    def test_knowledge_update_on_swap(self):
        """Knowledge should update to True after a swap."""
        self.player.set_in_hand(5) 
        self.player.swap_hand_with_inventory(0)
        self.assertTrue(self.player.player_knowledge[0])

if __name__ == '__main__':
    unittest.main()
