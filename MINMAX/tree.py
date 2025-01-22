from copy import deepcopy, copy
import pygame
from check.constants import RED, WHITE

"""
from concurrent.futures import ProcessPoolExecutor

def evaluate_move(move, depth, max_player, game, alpha, beta):
    # A helper function to evaluate a single move
    return minmaxtree(move, depth - 1, not max_player, game, alpha, beta)[0], move

def minmaxtree(position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
    if depth == 0 or position.winner() is not None:
        return position.score(), position

    position.set_sound_enabled(False)
    moves = get_all_moves(position, WHITE if max_player else RED, game)

    if not moves:
        return position.score(), position

    best_move = None
    if max_player:
        max_eval = float('-inf')
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(lambda move: evaluate_move(move, depth, max_player, game, alpha, beta), moves))

        for evaluation, move in results:
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = move
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        with ProcessPoolExecutor() as executor:
            results = list(executor.map(lambda move: evaluate_move(move, depth, max_player, game, alpha, beta), moves))

        for evaluation, move in results:
            if evaluation < min_eval:
                min_eval = evaluation
                best_move = move
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move

"""

# with alpha-beta pruning
def minmaxtree(position, depth, max_player, game, alpha = float('-inf'), beta = float('inf')): #(board object(board with all its details), how far are we making the tree(recursive), bool value (do we want max or min value), game object)
    
    if depth == 0 or position.winner() != None:
        position.set_sound_enabled(True) # re-enables sound                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return position.score(), position   # base case (if at base or game is won, return position and evaluation)

    position.set_sound_enabled(False) #disables sound for minmax tree                         !!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    s = position.score()
    best_move = None

    if max_player:
        max_eval = float('-inf') #(we want to determine the best, this is an initialization)
        #best_move = None
        
        for move in get_all_moves(position, WHITE, game): #gets all possible moves for position
            # if move.score() < s:       #testing to eliminate more moves
            #     continue

            evaluation = minmaxtree(move, depth - 1, False, game, alpha, beta)[0] #recursive call, [0] means it takes only the evaluation and not the path
            max_eval = max(max_eval, evaluation)
            
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
            
            if max_eval == evaluation: #if current move is the best move, set it equal to the move
                best_move = move 
        
        #position.set_sound_enabled(True) # re-enables sound                                     !!!!!!!!!!!!!!!!!!!!!!!!
        return max_eval, best_move 
    else:
        min_eval = float('inf') #(we want to determine the best, this is an initialization)
        #best_move = None

        for move in get_all_moves(position, RED, game): #gets all possible moves for position
            # if move.score() < s:      #testing to eliminate more moves
            #     continue

            evaluation = minmaxtree(move, depth - 1, True, game, alpha, beta)[0] #recursive call, [0] means it takes only the evaluation and not the path
            min_eval = min(min_eval, evaluation)
            
            # Perhaps here we could compute the current value of the board, and set these break conditions to be one or two less than
            # the current board value (or we could do an IDS-esque move where we look for the best move that doesn't involve us losing a
            # piece, but if that isn't possible, we begin looking for the best path in which we don't lose two, and so on.)

            beta = min(beta, min_eval)
            if beta <= alpha:
                break
            
            if min_eval == evaluation: #if current move is the best move, set it equal to the move
                best_move = move 
        
        #position.set_sound_enabled(True) # re-enables sound                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return min_eval, best_move    

def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1]) #(piece, row, column)
    if skip: # if we skipped over a piece
        board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = [] #list that stores new board
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        
        for move, skip in valid_moves.items(): 
            draw_moves(game, board, piece) # testttttttttttttt!!!!!!!!!
            temp_board = deepcopy(board) #copys the board to a temp variable                          
            temp_board.death_sound = pygame.mixer.Sound("death.mp3")  # Restore sound after deepcopy          !!!!!!!!!!
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip) #(takes the piece, the move we want to make, take the temp board, then stores what the board will look like)
            
            moves.append(new_board)

    return moves

#test
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)          #color green
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(25)