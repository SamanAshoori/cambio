import pygame
import sys
from cambio import Cambio
from player import Player

WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 90, 120
SPACE = 20
CARD_COLOUR = (255, 255, 255)
BACKGROUND_COLOUR = (0, 0, 0)
TEXT_COLOUR = (255, 255, 255)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cambio Game")
    clock = pygame.time.Clock()
    font = pygame.font.Font('Arial', 36)


    cambio = Cambio()
    running = True

    def draw_card(card,x,y):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(screen, CARD_COLOUR, rect,2)
        pygame.draw.rect(screen, BACKGROUND_COLOUR, rect, 2)

        card_text = cambio.convert_card(card)
        text = font.render(card_text, True, TEXT_COLOUR)

        text_rect = text.get_rect(center = (x + CARD_WIDTH // 2, y + CARD_HEIGHT // 2))
        screen.blit(text, text_rect)

    
    def draw_grid(inventory,start_X,start_Y):

        for i in range(4):
            row = i // 2
            col = i % 2
            x = start_X + col * (CARD_WIDTH + SPACE)
            y = start_Y + row * (CARD_HEIGHT + SPACE)

            if i < len(inventory):
                draw_card(inventory[i],x,y)
        
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                ##when space is pressed step is called
                if event.key == pygame.K_SPACE:
                    cambio.step()
        
        #draw
        screen.fill(BACKGROUND_COLOUR)
        #player one x and y
        p1_x = (WIDTH // 2) + CARD_WIDTH + SPACE
        p1_y = HEIGHT - 150

        #player 2 x and y 
        p2_x = (WIDTH // 2) - CARD_WIDTH - SPACE
        p2_y = 150
        
        label_p1 = font.render("Player 1", True, TEXT_COLOUR)
        label_p2 = font.render("Player 2", True, TEXT_COLOUR)
        screen.blit(label_p1, (WIDTH // 2 - 50, 20))
        screen.blit(label_p2, (WIDTH // 2 + 50, 20))

        draw_grid



        



        


