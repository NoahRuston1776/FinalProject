#If you want to exit the program, spam esc till you escape
#known issues are at the bottom of this file
import pygame
import time
from check.constants import WIDTH, HEIGHT, SQUARE_SIZE, FPS, WHITE, RED
from check.game import Game
from check.menu import menu
from check.piece import Piece
from MINMAX.tree import minmaxtree
from check.board import Board

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

clock = pygame.time.Clock()
def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = (x - Piece.offset) // SQUARE_SIZE        
    return row, col

def main():
    mode = menu(WIN)

    run = True
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        if mode == "AIvP":
            if game.turn == WHITE:
                value, new_board = minmaxtree(game.get_board(), 3, WHITE, game)         # to change the depth, change the second variable (set to 4 right now)
                game.AI_move(new_board)
            
    
        if mode == "AIvAI":                    # this doesnt work
            if game.turn == RED:
                print("RED's turn")
                value, new_board = minmaxtree(game.get_board(), 2, RED, game)
                game.AI_move(new_board)
            elif game.turn == WHITE:
                print("WHITE's turn")
                value, new_board = minmaxtree(game.get_board(), 2, WHITE, game)
                game.AI_move(new_board)

        winner = game.winner()
        if winner:      
            seconds = time.time()
            pygame.mixer.music.stop()
            if seconds == 20:      
                run = False
                pygame.display.quit()     
                pygame.quit()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:       
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    pygame.quit()
                    run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN: 
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                

        game.update()
    pygame.mixer.music.stop()
    pygame.quit() 

main()


# game issues

# issue with winning game flash has a bug, win isn't centered, cannot exit properly


# AI issues

# killing sound not playing for AI or for player when against AI
# AI vs AI not working (see for yourself)
# check for bug with AI with not always removing piece it jumps over when jumping more than one piece?
# make the AI faster and smarter

# stuff marked with !!!!!!!!!!!! are because they are parts of fixing some of the bugs, such as the first AI bug, just be careful pls :)