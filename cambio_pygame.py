import pygame
import sys
from cambio import Cambio

# setup screen dims
WIDTH, HEIGHT = 1280, 720
CARD_WIDTH, CARD_HEIGHT = 90, 120
SPACE = 10 

# colors
BACKGROUND_COLOUR = (34, 139, 34) # classic felt green
CARD_COLOUR = (255, 255, 255)     
CARD_BACK_COLOUR = (65, 105, 225) # Royal Blue for back of cards
BORDER_COLOUR = (0, 0, 0)         
TEXT_BLACK = (0, 0, 0)
TEXT_RED = (200, 0, 0)
EMPTY_SLOT_COLOUR = (30, 100, 30) 
WINNER_COLOUR = (255, 215, 0) # gold

def draw_card(screen, font, card_val, x, y, game_instance, hidden=False):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

    # if it's -2, it's an empty slot (no card)
    if card_val == -2:
        pygame.draw.rect(screen, EMPTY_SLOT_COLOUR, rect, border_radius=5)
        pygame.draw.rect(screen, (50, 120, 50), rect, 2, border_radius=5)
        return

    # if hidden is True, draw the back of the card
    if hidden:
        pygame.draw.rect(screen, CARD_BACK_COLOUR, rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=5) # white border for contrast
        # maybe add a little pattern or circle in the middle so it looks like a card back
        pygame.draw.circle(screen, (255,255,255), (x + CARD_WIDTH//2, y + CARD_HEIGHT//2), 10, 1)
        return

    # OTHERWISE: Draw the face of the card
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
            # LOGIC FOR HIDING CARDS
            should_hide = False

            if not game_over:
                if is_opponent:
                    # Always hide opponent cards during game
                    should_hide = True
                else:
                    # For Player 1, check if they "know" the card
                    # access the knowledge list directly from the player object
                    if not player.player_knowledge[i]:
                        should_hide = True
            
            # if game_over is True, should_hide stays False (reveal all)
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

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    result = cambio.step()
                    if result: 
                        game_over = True
                        winner_message = result

        # --- DRAWING ---
        screen.fill(BACKGROUND_COLOUR)

        grid_pixel_width = (CARD_WIDTH * 2) + SPACE

        # 1. Player 2 (Top)
        p2_x = (WIDTH - grid_pixel_width) // 2
        p2_y = 50 
        # Pass the whole player object, tell function it is_opponent=True
        draw_grid(screen, font, cambio.player_two, p2_x, p2_y, cambio, is_opponent=True, game_over=game_over)
        
        # P2 Label
        lbl_p2 = ui_font.render(f"Player 2", True, (255, 255, 255))
        screen.blit(lbl_p2, (WIDTH//2 - lbl_p2.get_width()//2, 20))


        # 2. Player 1 (Bottom)
        p1_x = (WIDTH - grid_pixel_width) // 2
        p1_y = HEIGHT - (CARD_HEIGHT * 2) - SPACE - 50
        # is_opponent=False
        draw_grid(screen, font, cambio.player_one, p1_x, p1_y, cambio, is_opponent=False, game_over=game_over)

        # P1 Label
        lbl_p1 = ui_font.render("Player 1 (You)", True, (255, 255, 255))
        screen.blit(lbl_p1, (WIDTH//2 - lbl_p1.get_width()//2, HEIGHT - 40))


        # 3. Deck and Discard
        center_y = HEIGHT // 2 - CARD_HEIGHT // 2
        
        # Deck
        deck_x = WIDTH // 2 - CARD_WIDTH - 20
        deck_rect = pygame.Rect(deck_x, center_y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 150), deck_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), deck_rect, 2, border_radius=5)
        
        # Discard
        if cambio.discard_pile:
            top_discard = cambio.discard_pile[-1]
            discard_x = WIDTH // 2 + 20
            # discard is never hidden
            draw_card(screen, font, top_discard, discard_x, center_y, cambio, hidden=False)

        # 4. GAME OVER STATE
        if game_over:
            # calculate final scores using your class methods
            p1_score = cambio.turn_deck_to_score(1)
            p2_score = cambio.turn_deck_to_score(2)

            # dim the screen slightly
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180) # higher alpha = darker
            overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))

            # Draw everything again on top? No, just draw text over the dimmed cards
            # Actually, we want to see the cards. 
            # So I won't use the full screen overlay, just a box for the text.

            # Winner Text
            win_text = winner_font.render(winner_message, True, WINNER_COLOUR)
            win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            screen.blit(win_text, win_rect)
            
            # Score Text
            score_str = f"P1 Score: {p1_score}  |  P2 Score: {p2_score}"
            score_text = font.render(score_str, True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            screen.blit(score_text, score_rect)

        else:
            # Game running instructions
            inst_text = ui_font.render("Press SPACE to step", True, (255, 255, 0))
            screen.blit(inst_text, (20, HEIGHT - 40))
            
            # turn counter
            turn_text = ui_font.render(f"Turn: {cambio.turn_count}", True, (200, 200, 200))
            screen.blit(turn_text, (20, 20))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()