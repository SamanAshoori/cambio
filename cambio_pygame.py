import pygame
import sys
from cambio import Cambio

# Constants
WIDTH, HEIGHT = 1280, 720
CARD_WIDTH, CARD_HEIGHT = 90, 120
SPACE = 10 

# Colors
BACKGROUND_COLOUR = (34, 139, 34) 
CARD_COLOUR = (255, 255, 255)     
CARD_BACK_COLOUR = (65, 105, 225) # Royal Blue
BORDER_COLOUR = (0, 0, 0)         
TEXT_BLACK = (0, 0, 0)
TEXT_RED = (200, 0, 0)
EMPTY_SLOT_COLOUR = (30, 100, 30) 
WINNER_COLOUR = (255, 215, 0)

# Animation Settings
ANIMATION_DELAY = 40 # Frames to wait (approx 1.5 seconds) to see the card

def draw_card(screen, font, card_val, x, y, game_instance, hidden=False):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

    # Empty Slot
    if card_val == -2:
        pygame.draw.rect(screen, EMPTY_SLOT_COLOUR, rect, border_radius=5)
        pygame.draw.rect(screen, (50, 120, 50), rect, 2, border_radius=5)
        return

    # Hidden Card (Back)
    if hidden:
        pygame.draw.rect(screen, CARD_BACK_COLOUR, rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=5)
        # Decorative circle
        pygame.draw.circle(screen, (255,255,255), (x + CARD_WIDTH//2, y + CARD_HEIGHT//2), 10, 1)
        return

    # Visible Card (Face)
    pygame.draw.rect(screen, CARD_COLOUR, rect, border_radius=5)
    pygame.draw.rect(screen, BORDER_COLOUR, rect, 2, border_radius=5)

    card_text = game_instance.convert_card(card_val)
    
    if "H" in card_text or "D" in card_text:
        text_color = TEXT_RED
    else:
        text_color = TEXT_BLACK

    text_surf = font.render(card_text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    screen.blit(text_surf, text_rect)

def draw_grid(screen, font, player, start_X, start_Y, game_instance, is_opponent, game_over):
    inventory = player.get_inventory()
    
    for i in range(4):
        row = i // 2  
        col = i % 2   
        
        x = start_X + col * (CARD_WIDTH + SPACE)
        y = start_Y + row * (CARD_HEIGHT + SPACE)

        if i < len(inventory):
            should_hide = False
            if not game_over:
                # Hide if it's opponent OR if it's Player 1 and they don't know the card
                if is_opponent or (not is_opponent and not player.player_knowledge[i]):
                    should_hide = True
            
            draw_card(screen, font, inventory[i], x, y, game_instance, hidden=should_hide)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cambio Game")
    clock = pygame.time.Clock()
    
    font = pygame.font.SysFont("Arial", 36, bold=True)
    ui_font = pygame.font.SysFont("Arial", 24)
    winner_font = pygame.font.SysFont("Arial", 60, bold=True)

    cambio = Cambio()
    running = True
    game_over = False
    winner_message = ""

    # Animation State Variables
    turn_phase = "IDLE" # IDLE, DRAW, THINK, ACTION
    anim_timer = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    if turn_phase == "IDLE":
                        turn_phase = "DRAW"

        # --- LOGIC UPDATE (The "Step" broken down) ---
        
        # 1. DRAW PHASE: Card moves from Deck to Hand
        if turn_phase == "DRAW":
            if len(cambio.deck) == 0:
                game_over = True
                winner_message = cambio.get_winner()
            else:
                cambio.turn_count += 1
                # Manually call draw
                cambio.player_get_card_from_pile(cambio.current_player_turn)
                # Start timer for visual pause
                anim_timer = ANIMATION_DELAY 
                turn_phase = "THINK"
        
        # 2. THINK PHASE: Pause so we can see the card (or see P2 thinking)
        elif turn_phase == "THINK":
            if anim_timer > 0:
                anim_timer -= 1
            else:
                turn_phase = "ACTION"

        # 3. ACTION PHASE: Swap or Discard
        elif turn_phase == "ACTION":
            current_p_obj = cambio.player_one if cambio.current_player_turn == 1 else cambio.player_two
            
            # AI/Logic decides what to do
            swap_index = current_p_obj.decide_swap_index()
            
            if swap_index != -1:
                cambio.player_put_card_in_hand_into_deck(swap_index, cambio.current_player_turn)
            else:
                if current_p_obj.get_in_hand() != -2:
                    cambio.discard(cambio.current_player_turn)

            # Switch Turn
            cambio.current_player_turn = 2 if cambio.current_player_turn == 1 else 1
            turn_phase = "IDLE"


        # --- DRAWING ---
        screen.fill(BACKGROUND_COLOUR)
        grid_pixel_width = (CARD_WIDTH * 2) + SPACE

        # Draw Player 2
        p2_x = (WIDTH - grid_pixel_width) // 2
        p2_y = 50 
        draw_grid(screen, font, cambio.player_two, p2_x, p2_y, cambio, is_opponent=True, game_over=game_over)
        
        # Draw Player 1
        p1_x = (WIDTH - grid_pixel_width) // 2
        p1_y = HEIGHT - (CARD_HEIGHT * 2) - SPACE - 50
        draw_grid(screen, font, cambio.player_one, p1_x, p1_y, cambio, is_opponent=False, game_over=game_over)

        # Labels
        lbl_p2 = ui_font.render(f"Player 2", True, (255, 255, 255))
        screen.blit(lbl_p2, (WIDTH//2 - lbl_p2.get_width()//2, 20))
        lbl_p1 = ui_font.render("Player 1 (You)", True, (255, 255, 255))
        screen.blit(lbl_p1, (WIDTH//2 - lbl_p1.get_width()//2, HEIGHT - 40))


        # Deck and Discard
        center_y = HEIGHT // 2 - CARD_HEIGHT // 2
        deck_x = WIDTH // 2 - CARD_WIDTH - 20
        
        # Draw Deck
        deck_rect = pygame.Rect(deck_x, center_y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 150), deck_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), deck_rect, 2, border_radius=5)
        
        # Draw Discard Pile
        if cambio.discard_pile:
            top_discard = cambio.discard_pile[-1]
            discard_x = WIDTH // 2 + 20
            draw_card(screen, font, top_discard, discard_x, center_y, cambio, hidden=False)

        # --- ANIMATION: DRAW THE CARD IN HAND ---
        # If we are in the "THINK" phase, a player is holding a card. Let's show it!
        if turn_phase == "THINK":
            active_player = cambio.current_player_turn
            current_p_obj = cambio.player_one if active_player == 1 else cambio.player_two
            held_card = current_p_obj.get_in_hand()
            
            # Position for the "Hand" card
            # If P1: Draw it floating above their inventory
            # If P2: Draw it floating below their inventory
            if active_player == 1:
                hand_x = WIDTH // 2 - CARD_WIDTH // 2
                hand_y = p1_y - CARD_HEIGHT - 20
                draw_card(screen, font, held_card, hand_x, hand_y, cambio, hidden=False)
            else:
                hand_x = WIDTH // 2 - CARD_WIDTH // 2
                hand_y = p2_y + (CARD_HEIGHT*2) + SPACE + 20
                # CRITICAL CHANGE: Hide P2's card!
                draw_card(screen, font, held_card, hand_x, hand_y, cambio, hidden=True)

        # Game Over / Instructions
        if game_over:
            p1_score = cambio.turn_deck_to_score(1)
            p2_score = cambio.turn_deck_to_score(2)

            win_text = winner_font.render(winner_message, True, WINNER_COLOUR)
            win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            # Text Outline for readability
            pygame.draw.rect(screen, BACKGROUND_COLOUR, win_rect) 
            screen.blit(win_text, win_rect)
            
            score_str = f"P1: {p1_score}  |  P2: {p2_score}"
            score_text = font.render(score_str, True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            pygame.draw.rect(screen, BACKGROUND_COLOUR, score_rect)
            screen.blit(score_text, score_rect)
        
        else:
            if turn_phase == "IDLE":
                inst_text = ui_font.render("Press SPACE to take a turn", True, (255, 255, 0))
                screen.blit(inst_text, (20, HEIGHT - 40))
            elif turn_phase == "THINK":
                txt = "Thinking..." if cambio.current_player_turn == 2 else "You drew a card..."
                status_text = ui_font.render(txt, True, (200, 200, 200))
                screen.blit(status_text, (20, HEIGHT - 40))

            turn_text = ui_font.render(f"Turn: {cambio.turn_count}", True, (200, 200, 200))
            screen.blit(turn_text, (20, 20))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()