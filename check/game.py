import pygame
from .board import Board
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, HEIGHT, WIDTH, ROWS

#for winner function
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.font.init()

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.move_sound = pygame.mixer.Sound("move.mp3")
        self.win_sound = pygame.mixer.Sound("FNAF.mp3")
        self.first_time = True
        self.offset = (WIDTH - HEIGHT) // 2    

    def play_winning_music(self):
        self.win_sound.play()  # Play the winning sound
        self.win_sound.set_volume(0.5)

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):           # _ makes it private
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
    
    def winner(self):
        font = pygame.font.Font(None, 74)
        winner = self.board.winner()
        if winner and self.first_time:
            self.play_winning_music()
            self.first_time = False
        if winner:
            #self.play_winning_music()
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # Black overlay with 150 alpha for shading
            WIN.blit(overlay, (0, 0))
            # Flashing text loop for winner
            while True:
                flash_on = True
                if flash_on:
                    text_color = WHITE if winner == WHITE else RED
                    text_message = "WHITE WON" if winner == WHITE else "RED WON"
                    text = font.render(text_message, True, text_color)
                    WIN.blit(text, (WIDTH / 3, HEIGHT / 2.1))
                pygame.display.update()  # Update the display
                pygame.time.delay(500)

                flash_on = False
                if flash_on == False:
                    WIN.fill((0,0,0))
                    self.update()
                    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                    overlay.fill((0, 0, 0, 150))  # Black overlay with 150 alpha for shading
                    WIN.blit(overlay, (0, 0))
                    
                pygame.display.update()
                # Display the winner text
                pygame.time.delay(500)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                return True 
    
    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col) 
            if not result:
                self.selected = None
                self.select(row, col)
                
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False

    def _move(self, row, col):         # _ makes it private
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            self.move_sound.play()
            self.move_sound.set_volume(1)
        else:
            return False
        return True
        
    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (self.offset + col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)        

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):  #returns the board object for min max tree
        return self.board
    
    def AI_move(self, board): #updates the board after the AI's move
        self.board = board
        self.move_sound.play()
        self.move_sound.set_volume(1)
        #self.board.set_sound_enabled(True)                                   !!!!!!!!!!!!!!
        self.change_turn()