import pygame
import math
from copy import deepcopy, copy
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE, WIDTH, HEIGHT
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []   # stores the board, if a piece is at a position it stores a piece object, Piece(), or a 0 if empty
        self.red_left = self.white_left = math.floor(3 / 8 * ROWS) * COLS // 2 #calculates the number of pieces needed
        self.red_kings = self.white_kings = 0
        self.create_board()
        self.death_sound = pygame.mixer.Sound("death.mp3")
        self.sound_enabled = True # for AI                               !!!!!!!!!!!!!!!
        self.offset = (WIDTH - HEIGHT) // 2 

    def set_sound_enabled(self, enabled):      #for AI
        self.sound_enabled = enabled                                 #!!!!!!!!!!

    def __deepcopy__(self, memo):                      # for AI       !!!!!!!!!!!!!!!!!!!!!
        # Create a shallow copy of the object first
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        # Copy each attribute, except for unpicklable ones (sounds)
        for k, v in self.__dict__.items():
            if k == "death_sound":  # Skip the sound object
                setattr(result, k, None)
            else:
                setattr(result, k, deepcopy(v, memo))
        return result

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (self.offset + col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))      
    
    def score(self):     # central needs to be adjusted to all board sizes
        difference = self.white_left - self.red_left         #difference in pieces
        
        kings = (self.white_kings - self.red_kings) * 0.5    #difference in kings

       # promotion = sum(piece.row for piece in self.get_all_pieces(WHITE)) - sum((ROWS - 1 - piece.row) for piece in self.get_all_pieces(RED)) #something wrong in here    # awards points by encouraging promotion
    
        column = sum(abs(COLS // 2 - piece.col) for piece in self.get_all_pieces(WHITE)) - sum(abs(COLS // 2 - piece.col) for piece in self.get_all_pieces(RED))   #awards points for being in center of board

        return (difference + kings + 0.05 * column)# + 0.1 * promotion)

    """
    def score(self): #calculates the score of the current board state for the min max tree
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)   # we can make this more complicated!!!!!
    """
    def get_all_pieces(self, color): #gets all pieces of a color for the min max algorithm
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            if piece.king == False:             # makes sure counter isn't increased if piece is already king
                piece.make_king()
                if piece.color == WHITE:
                    self.white_kings += 1
                else:
                    self.red_kings += 1 
        
    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        white_rows = math.floor(3 / 8 * ROWS)
        red_rows = white_rows + 1
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < white_rows:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > red_rows:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                    print("RED PIECES LEFT: ") #outputs # of red pieces to terminal
                    print(self.red_left)
                else:
                    self.white_left -= 1
                    print("WHITE PIECES LEFT: ") #outputs # of white pieces to terminal
                    print(self.white_left)
       # if self.sound_enabled and self.death_sound: # For AI sound                          !!!!!!!!!!!!!!!!!
        if self.sound_enabled:  
            self.death_sound.play()
            self.death_sound.set_volume(1)

    def winner(self):
        # checks of there are any colors left
        if self.red_left == 0:
            return WHITE
        elif self.white_left == 0:
            return RED
        else:
            # Checks if either player has no valid moves
            red_valid_moves = False
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if piece != 0 and piece.color == RED:
                        if self.get_valid_moves(piece):  
                            red_valid_moves = True
                            break
                if red_valid_moves:
                    break

            white_valid_moves = False
            for row in range(ROWS):
                for col in range(COLS):
                    piece = self.board[row][col]
                    if piece != 0 and piece.color == WHITE:
                        if self.get_valid_moves(piece):  
                            white_valid_moves = True
                            break
                if white_valid_moves:
                    break

            if not red_valid_moves:
                return WHITE
            elif not white_valid_moves:
                return RED

            return None  

    def get_valid_moves(self, piece):                  
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row          
        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
            #print(moves)
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves


    def _traverse_left(self, start, stop, step, color, left, skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.board[r][left]   # Current index of the piece on the board
            if current == 0:
                if skipped and not last:       # If a piece has been jumped already and you haven't already made a move
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)  # This is where the error was. For some reason this needed to be a -1. - Ben
                    else:
                        row = min(r + 3, ROWS)
                    
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped = last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped = last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, skipped = []):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                    else:
                        row = min(r + 3, ROWS)
                    
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped = last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped = last))
                break

            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        return moves
