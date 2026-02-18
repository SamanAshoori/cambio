import pygame
import sys
from cambio import Cambio

# Constants
WIDTH, HEIGHT = 720, 1280
CARD_WIDTH, CARD_HEIGHT = 90, 120
SPACE = 10 
GAME_SPEED_DELAY = 200 # Milliseconds between turns (Lower = Faster)

# Colors
BACKGROUND_COLOUR = (34, 139, 34) 
CARD_COLOUR = (255, 255, 255)     
CARD_BACK_COLOUR = (65, 105, 225) 
BORDER_COLOUR = (0, 0, 0)         
TEXT_BLACK = (0, 0, 0)
TEXT_RED = (200, 0, 0)
EMPTY_SLOT_COLOUR = (30, 100, 30) 
WINNER_COLOUR = (255, 215, 0)

def draw_card(screen, font, card_val, x, y, game_instance, hidden=False):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
    if card_val == -2:
        pygame.draw.rect(screen, EMPTY_SLOT_COLOUR, rect, border_radius=5)
        pygame.draw.rect(screen, (50, 120, 50), rect, 2, border_radius=5)
        return
    if hidden:
        pygame.draw.rect(screen, CARD_BACK_COLOUR, rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=5)
        pygame.draw.circle(screen, (255,255,255), (x + CARD_WIDTH//2, y + CARD_HEIGHT//2), 10, 1)
        return
    pygame.draw.rect(screen, CARD_COLOUR, rect, border_radius=5)
    pygame.draw.rect(screen, BORDER_COLOUR, rect, 2, border_radius=5)
    card_text = game_instance.convert_card(card_val)
    text_color = TEXT_RED if "H" in card_text or "D" in card_text else TEXT_BLACK
    text_surf = font.render(card_text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    screen.blit(text_surf, text_rect)

def draw_grid(screen, font, player, start_X, start_Y, game_instance, is_opponent, game_over):
    inventory = player.get_inventory()
    for i in range(len(inventory)):
        row = i // 2  
        col = i % 2   
        x = start_X + col * (CARD_WIDTH + SPACE)
        y = start_Y + row * (CARD_HEIGHT + SPACE)
        if i < len(inventory):
            should_hide = False
            if not game_over:
                if is_opponent or (not is_opponent and not player.player_knowledge[i]):
                    should_hide = True
            draw_card(screen, font, inventory[i], x, y, game_instance, hidden=should_hide)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cambio Game - AUTO RUN TEST")
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
        
        # --- AUTO RUN LOGIC ---
        if not game_over:
            # DIRECTLY CALL STEP FROM CAMBIO.PY
            # This ensures 100% logic parity
            result = cambio.step()
            
            if result:
                game_over = True
                winner_message = result
            
            # Artificial delay so we can watch it happen
            pygame.time.delay(GAME_SPEED_DELAY)

        # --- DRAWING ---
        screen.fill(BACKGROUND_COLOUR)
        grid_pixel_width = (CARD_WIDTH * 2) + SPACE

        p2_x = (WIDTH - grid_pixel_width) // 2
        p2_y = 50 
        draw_grid(screen, font, cambio.player_two, p2_x, p2_y, cambio, is_opponent=True, game_over=game_over)
        
        p1_x = (WIDTH - grid_pixel_width) // 2
        p1_y = HEIGHT - (CARD_HEIGHT * 2) - SPACE - 150
        draw_grid(screen, font, cambio.player_one, p1_x, p1_y, cambio, is_opponent=False, game_over=game_over)

        lbl_p2 = ui_font.render(f"Player 2 (AI)", True, (255, 255, 255))
        screen.blit(lbl_p2, (WIDTH//2 - lbl_p2.get_width()//2, 20))
        lbl_p1 = ui_font.render("Player 1 (AI Testing)", True, (255, 255, 255))
        screen.blit(lbl_p1, (WIDTH//2 - lbl_p1.get_width()//2, HEIGHT - 40))

        center_y = HEIGHT // 2 - CARD_HEIGHT // 2
        deck_x = WIDTH // 2 - CARD_WIDTH - 20
        deck_rect = pygame.Rect(deck_x, center_y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 150), deck_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), deck_rect, 2, border_radius=5)
        
        if cambio.discard_pile:
            top_discard = cambio.discard_pile[-1]
            discard_x = WIDTH // 2 + 20
            draw_card(screen, font, top_discard, discard_x, center_y, cambio, hidden=False)

        if game_over:
            p1_score = cambio.turn_deck_to_score(1)
            p2_score = cambio.turn_deck_to_score(2)
            win_text = winner_font.render(winner_message, True, WINNER_COLOUR)
            win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
            pygame.draw.rect(screen, BACKGROUND_COLOUR, win_rect) 
            screen.blit(win_text, win_rect)
            
            score_str = f"P1: {p1_score}  |  P2: {p2_score}"
            score_text = font.render(score_str, True, (255, 255, 255))
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
            pygame.draw.rect(screen, BACKGROUND_COLOUR, score_rect)
            screen.blit(score_text, score_rect)
        else:
            turn_text = ui_font.render(f"Turn: {cambio.turn_count}", True, (200, 200, 200))
            screen.blit(turn_text, (20, 20))
            status_text = ui_font.render("AUTO-RUNNING...", True, (255, 255, 0))
            screen.blit(status_text, (20, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(20)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()