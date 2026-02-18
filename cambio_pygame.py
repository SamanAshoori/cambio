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
BORDER_COLOUR = (0, 0, 0)         
TEXT_BLACK = (0, 0, 0)
TEXT_RED = (200, 0, 0)
EMPTY_SLOT_COLOUR = (30, 100, 30) # darker green for empty spots
WINNER_COLOUR = (255, 215, 0) # gold for the winner text

def draw_card(screen, font, card_val, x, y, game_instance):
    rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

    # -2 means the player swapped it or discarded it, so draw an empty box
    if card_val == -2:
        pygame.draw.rect(screen, EMPTY_SLOT_COLOUR, rect, border_radius=5)
        pygame.draw.rect(screen, (50, 120, 50), rect, 2, border_radius=5)
        return

    # draw the white card background
    pygame.draw.rect(screen, CARD_COLOUR, rect, border_radius=5)
    
    # draw the border
    pygame.draw.rect(screen, BORDER_COLOUR, rect, 2, border_radius=5)

    # convert the int to something readable like 'KS' or '10H'
    card_text = game_instance.convert_card(card_val)
    
    # make hearts and diamonds red, everything else black
    if "H" in card_text or "D" in card_text:
        text_color = TEXT_RED
    else:
        text_color = TEXT_BLACK

    # render the text and center it
    text_surf = font.render(card_text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
    screen.blit(text_surf, text_rect)

def draw_grid(screen, font, inventory, start_X, start_Y, game_instance):
    # loop through the 4 cards and place them in a 2x2 grid
    for i in range(4):
        row = i // 2  
        col = i % 2   
        
        x = start_X + col * (CARD_WIDTH + SPACE)
        y = start_Y + row * (CARD_HEIGHT + SPACE)

        # only draw if the index actually exists
        if i < len(inventory):
            draw_card(screen, font, inventory[i], x, y, game_instance)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cambio Game")
    clock = pygame.time.Clock()
    
    # using Arial because the default font is kinda ugly
    font = pygame.font.SysFont("Arial", 36, bold=True)
    ui_font = pygame.font.SysFont("Arial", 24)
    winner_font = pygame.font.SysFont("Arial", 60, bold=True)

    cambio = Cambio()
    running = True
    winner_message = None # keeps track of who won

    while running:
        # --- input handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # only step if the game isn't over yet
                    if not winner_message:
                        result = cambio.step()
                        # if step returns a string, the game is done
                        if result: 
                            winner_message = result

        # --- drawing stuff ---
        screen.fill(BACKGROUND_COLOUR)

        # math to center the grids horizontally
        grid_pixel_width = (CARD_WIDTH * 2) + SPACE

        # 1. Player 2 (opponent at the top)
        p2_x = (WIDTH - grid_pixel_width) // 2
        p2_y = 50 
        draw_grid(screen, font, cambio.player_two.get_inventory(), p2_x, p2_y, cambio)
        
        # P2 Label
        lbl_p2 = ui_font.render(f"Player 2 (Turn: {cambio.turn_count})", True, (255, 255, 255))
        screen.blit(lbl_p2, (WIDTH//2 - lbl_p2.get_width()//2, 20))


        # 2. Player 1 (you at the bottom)
        p1_x = (WIDTH - grid_pixel_width) // 2
        p1_y = HEIGHT - (CARD_HEIGHT * 2) - SPACE - 50
        draw_grid(screen, font, cambio.player_one.get_inventory(), p1_x, p1_y, cambio)

        # P1 Label
        lbl_p1 = ui_font.render("Player 1", True, (255, 255, 255))
        screen.blit(lbl_p1, (WIDTH//2 - lbl_p1.get_width()//2, HEIGHT - 40))


        # 3. Deck and Discard (middle of the screen)
        center_y = HEIGHT // 2 - CARD_HEIGHT // 2
        
        # draw the deck (blue back)
        deck_x = WIDTH // 2 - CARD_WIDTH - 20
        deck_rect = pygame.Rect(deck_x, center_y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(screen, (0, 0, 150), deck_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), deck_rect, 2, border_radius=5)
        
        # draw discard pile if there's anything in it
        if cambio.discard_pile:
            top_discard = cambio.discard_pile[-1]
            discard_x = WIDTH // 2 + 20
            draw_card(screen, font, top_discard, discard_x, center_y, cambio)

        # 4. Instructions or Game Over screen
        if winner_message:
            # darken the background a bit so the text pops
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill((0,0,0))
            screen.blit(overlay, (0,0))

            # render the winner text
            win_text = winner_font.render(winner_message, True, WINNER_COLOUR)
            win_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(win_text, win_rect)
            
            # small helper text
            sub_text = ui_font.render("Close window to exit", True, (200, 200, 200))
            sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            screen.blit(sub_text, sub_rect)
        else:
            # game is still going
            inst_text = ui_font.render("Press SPACE to take a step", True, (255, 255, 0))
            screen.blit(inst_text, (20, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()