import pygame
import time
from .constants import WIDTH, HEIGHT, WHITE, RED,  BLACK
from .board import Board
from .game import Game
from.piece import Piece

pygame.mixer.init()
pygame.font.init()

MUSIC_FILES = {
    "PvP": "PvsP.mp3",
    "AIvAI": "AIvsAI.mp3",
    "AIvP": "AIvsP.mp3"
}

def play_music(mode):
    pygame.mixer.music.stop()  # Stop any music that's currently playing
    pygame.mixer.music.load(MUSIC_FILES[mode])  # Load music for the selected mode
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)

def draw_menu(WIN):
    board = Board()
    board.draw_squares(WIN)
    font = pygame.font.Font(None, 150)
    
    # Title
    checkers = font.render("Checkers", True, BLACK)
    pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 250, HEIGHT // 2 - 300, 500, 100), 0 , 20)
    pygame.draw.rect(WIN, BLACK, (WIDTH // 2 - 250, HEIGHT // 2 - 300, 500, 100), 5 , 20)
    WIN.blit(checkers,(WIDTH // 2 - checkers.get_width() // 2, HEIGHT // 2 - 298))
    
    font = pygame.font.Font(None, 74)
    # Draw buttons
    pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 105, HEIGHT // 2 - 100, 210, 50), 0, 20)
    pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 105, HEIGHT // 2, 210, 50), 0, 20)
    pygame.draw.rect(WIN, WHITE, (WIDTH // 2 - 105, HEIGHT // 2 + 100, 210, 50), 0, 20)
    pygame.draw.rect(WIN, BLACK, (WIDTH // 2 - 105, HEIGHT // 2 - 100, 210, 50), 2, 20)
    pygame.draw.rect(WIN, BLACK, (WIDTH // 2 - 105, HEIGHT // 2, 210, 50), 2, 20)
    pygame.draw.rect(WIN, BLACK, (WIDTH // 2 - 105, HEIGHT // 2 + 100, 210, 50), 2, 20)

    # Button text
    text_ai_vs_ai = font.render("AI vs AI", True, BLACK)
    text_ai_vs_p = font.render("AI vs P", True, BLACK)
    text_p_vs_p = font.render("P vs P", True, BLACK)

    # Position text
    WIN.blit(text_ai_vs_ai, (WIDTH // 2 - text_ai_vs_ai.get_width() // 2, HEIGHT // 2 - 97))
    WIN.blit(text_ai_vs_p, (WIDTH // 2 - text_ai_vs_p.get_width() // 2, HEIGHT // 2 + 5))
    WIN.blit(text_p_vs_p, (WIDTH // 2 - text_p_vs_p.get_width() // 2, HEIGHT // 2 + 105))

    pygame.display.update()

def menu(win):
    run = True
    mode = None

    pygame.mixer.music.load('menu.mp3')
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(loops=-1)

    while run:
        draw_menu(win)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None  # Exit the game entirely
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                
                # Check which button was clicked
                if WIDTH // 2 - 100 <= x <= WIDTH // 2 + 100:
                    if HEIGHT // 2 - 100 <= y <= HEIGHT // 2 - 50:
                        mode = "AIvAI"
                    elif HEIGHT // 2 <= y <= HEIGHT // 2 + 50:
                        mode = "AIvP"
                    elif HEIGHT // 2 + 100 <= y <= HEIGHT // 2 + 150:
                        mode = "PvP"
                
                if mode:
                    pygame.mixer.music.stop()
                    play_music(mode)
                    return mode