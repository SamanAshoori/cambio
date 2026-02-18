import unittest
from player import Player

class TestPlayerRiskLogic(unittest.TestCase):
    def setUp(self):
        print("\n" + "="*60)
        # Setup a player with 4 cards
        # Cards: 10 (Jack, score 10), 4 (5, score 5), 11 (Queen, score 10), 1 (2, score 2)
        self.inventory = [10, 4, 11, 1] 
        self.player = Player(self.inventory, "Test Player")
        
        # Reset knowledge to all False (default)
        self.player.player_knowledge = [False, False, False, False]
        
        # Set a standard risk tolerance
        self.player.set_risk_tolerance(6)
        print(f"SETUP: Inventory: {self.inventory}")
        print(f"SETUP: Knowledge: {self.player.player_knowledge}")
        print(f"SETUP: Risk Tolerance: {self.player.risk_tolerance}")

    def test_unknown_card_high_hand_value(self):
        print("TEST: Unknown card vs High Hand Value")
        """
        If we have a high value card in hand (King, score 10) and don't know the inventory card,
        we should NOT swap because 10 is not less than risk tolerance (6).
        """
        self.player.set_in_hand(12) # King of Spades (Score 10)
        print(f"ACTION: Set hand to King (12), Score: {self.player.get_card_score(12)}")
        
        idx = self.player.decide_swap_index()
        print(f"RESULT: Decided swap index: {idx}")
        self.assertEqual(idx, -1, "Should not swap a high value card for an unknown card")
        print("ASSERT: Passed (Index is -1)")

    def test_unknown_card_low_hand_value(self):
        print("TEST: Unknown card vs Low Hand Value")
        """
        If we have a low value card in hand (3, score 3) and don't know the inventory card,
        we SHOULD swap because 3 is less than risk tolerance (6).
        """
        self.player.set_in_hand(2) # 3 of Spades (Score 3)
        print(f"ACTION: Set hand to 3 (2), Score: {self.player.get_card_score(2)}")
        
        idx = self.player.decide_swap_index()
        print(f"RESULT: Decided swap index: {idx}")
        
        # It should return a valid index (not -1)
        self.assertNotEqual(idx, -1, "Should swap a low value card for an unknown card")
        # Since it iterates 0..3 and all are unknown, it should pick the first one (index 0)
        self.assertEqual(idx, 0)
        print("ASSERT: Passed (Index is 0)")

    def test_known_card_logic(self):
        print("TEST: Known High Card in Inventory vs Low Hand Value")
        """
        If we KNOW a card in inventory is high (Jack, score 10), and we have a lower card (5),
        we should swap regardless of risk tolerance because we know it's a good trade.
        """
        # Let's make index 0 known. Card at index 0 is 10 (Jack, score 10).
        self.player.player_knowledge[0] = True
        print(f"ACTION: Set knowledge at index 0 to True. Card is {self.inventory[0]} (Score: {self.player.get_card_score(self.inventory[0])})")
        
        # Hand has a 5 (score 5).
        self.player.set_in_hand(4) 
        print(f"ACTION: Set hand to 5 (4), Score: {self.player.get_card_score(4)}")
        
        # Logic: Known card (10) > Hand (5). Should swap.
        idx = self.player.decide_swap_index()
        print(f"RESULT: Decided swap index: {idx}")
        
        self.assertEqual(idx, 0, "Should swap because known inventory card is higher value")
        print("ASSERT: Passed (Index is 0)")

    def test_skip_known_bad_swap_for_unknown_risk(self):
        print("TEST: Skip Known Bad Swap, Take Unknown Risk")
        """
        If index 0 is KNOWN to be a 2 (bad swap), it should skip it.
        If index 1 is UNKNOWN, it should check risk tolerance.
        """
        # Change index 0 to a 2 of Spades (Score 2) and make it known
        self.player.player_inventory[0] = 1 
        self.player.player_knowledge[0] = True 
        print(f"ACTION: Modified Inventory[0] to 2 (1). Knowledge[0] = True.")
        
        # Hand is 5 of Spades (Score 5). Risk is 6.
        self.player.set_in_hand(4)
        print(f"ACTION: Set hand to 5 (4), Score: {self.player.get_card_score(4)}")
        
        idx = self.player.decide_swap_index()
        print(f"RESULT: Decided swap index: {idx}")
        
        # Index 0: Known (2). 2 > 5 is False. Skip.
        # Index 1: Unknown. Hand (5) < Risk (6) is True. Pick.
        self.assertEqual(idx, 1, "Should skip known bad swap (index 0) and take risk on unknown (index 1)")
        print("ASSERT: Passed (Index is 1)")

    def test_knowledge_update_on_swap(self):
        print("TEST: Knowledge Update on Swap")
        self.assertFalse(self.player.player_knowledge[0])
        print(f"CHECK: Initial knowledge at index 0 is {self.player.player_knowledge[0]}")
        
        self.player.set_in_hand(5) 
        print("ACTION: Swapping hand with inventory index 0")
        self.player.swap_hand_with_inventory(0)
        
        self.assertTrue(self.player.player_knowledge[0], "Knowledge should be True after swapping")
        print(f"CHECK: Post-swap knowledge at index 0 is {self.player.player_knowledge[0]}")
        print("ASSERT: Passed")

if __name__ == '__main__':
    unittest.main()
