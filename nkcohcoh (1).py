<<<<<<< HEAD
#https://www.cs.swarthmore.edu/~meeden/cs63/f05/minimax.html (pseudocode from here)
#http://codereview.stackexchange.com/a/24775 (ideas for victory check)

#things to try for alpha-beta:
#transposition table
#use of IDS to order branch exploration

import sys
import numpy as np
import copy

losing_seq = []
  
def printable_board(board):
  return "\n".join([ " ".join(row) for row in board])
  
def sequences(n, k):
  positions_groups = []
  seq = (
    [[[(x, y+z) for y in range(k)] for z in range(n-k+1) ] for x in range(n)] + # horizontals
    [[[(x+z, y) for x in range(k)] for z in range(n-k+1) ] for y in range(n)] + # verticals
    [[[(d+x, d+z) for d in range(k)] for x in range(n-k+1) ] for z in range(n-k+1)] + #diag TL BR
    [[[(n-1-d-x, d+z) for d in range(k)] for x in range(n-k+1) ] for z in range(n-k+1)] # diagonal BL TR
  )
  for s in seq:
   for d in s:
    positions_groups.append(d)
  return np.array(positions_groups)

def game_heuristic(board, n, k):
  
  return 0

# Check whether game has ended and whether there is a tie, a win, or a lose
def game_status(board, n, k):
  for seq in losing_seq:
    vals = [ board[x,y] for [x,y] in seq ]
    if all(v == 'b' for v in vals): return True, 1
    if all(v == 'w' for v in vals): return True, -1
  if all('.' not in row for row in board): return True, 0
  return False, game_heuristic(board, n, k)
    
# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col, color):
    newboard = copy.deepcopy(board)
    newboard[row,col] = color
    return newboard
  
def successor(board, color):
  empty = zip(*np.where(board == '.'))
  return [ add_piece(board, row, col, color) for (row, col) in empty ]

#need to implement this
def branching_factor_function(time):
  return 100

def alphaBetaSearch(board, n, k, time):
  order = {}
  depth_limit = branching_factor_function(time)
  val, newboard = alphaBetaMinimax(board, n, k, -sys.maxsize, sys.maxsize, depth_limit, 0, order)
  return newboard
  
def alphaBetaSearchIDS(board, n, k, time):
  max_depth = branching_factor_function(time)
  # hash table to store move order
  order = {}
  depth = 1
  while depth < depth_limit:
    alphaBetaMinimax(board, n, k, -sys.maxsize, sys.maxsize, depth, 0, order)
    depth += 1

def alphaBetaMinimax(board, n, k, alpha, beta, depth_limit, depth, order):
  #check for leaf nodes
  end, status = game_status(board, n, k)
  if end is True: return status, board
  if depth >= depth_limit: return status, board
  #find whose turn it is
  color = 'b' if len(board[board == 'w']) > len(board[board == 'b']) else 'w'
  # get successors
  successors = successor(board, color)
  # keep only ordered successors if this depth has already been explored:
  if str(board) in order: successors = [ successors[i] for i in order[ str(board) ] ]
  # keep track of best move for current player
  best_move = []
  # keep track of scores for each successor
  scores = []
  #if MAX's turn
  if color == 'w':
    print("depth", depth, "MAX:", "alpha", alpha, "beta", beta)
    for s in successors:
      result, newboard = alphaBetaMinimax(s, n, k, alpha, beta, depth_limit, depth+1, order)
      scores.append(result)
      if result > alpha:
        alpha = result
        best_move = s
      if alpha >= beta:
        return alpha, best_move
    # store moves in decreasing value order
    if str(board) not in order: order[str(board)] = sorted(range(len(scores)), key=lambda k: scores[k], reverse = True)
    print("depth", depth, "MAX:", "alpha", alpha, "beta", beta)
    print("current board")
    print(printable_board(board))
    print ("successors MAX\n", "\n\n".join([printable_board(i) for i in successors]), "scores", scores)
    return alpha, best_move
  #if MIN's turn
  if color == 'b':
    for s in successors:
      result, newboard = alphaBetaMinimax(s, n, k, alpha, beta, depth_limit, depth+1, order)
      scores.append(result)
      if result < beta:
        beta = result
        best_move = s
      if alpha >= beta:
        return beta, best_move
    # store moves in increasing value order
    if str(board) not in order: order[str(board)] = order[str(board)] = sorted(range(len(scores)), key=lambda k: scores[k])
    print("depth", depth, "MIN:", "alpha", alpha, "beta", beta)
    print("current board")
    print(printable_board(board))
    print ("successors MAX\n", "\n\n".join([printable_board(i) for i in successors]), "scores", scores)
    return beta, best_move
    
if "__main__" == __name__:
  n, k, board, time = int(sys.argv[1]), int(sys.argv[2]), str(sys.argv[3]),  int(sys.argv[4])
  losing_seq = sequences(n,k)
  board = np.reshape(list(board), (n, n))
  print ( "current board:")
  print (printable_board(board))
  end, status = game_status(board, n, k)
  result = ": white won." if status == 1 else ": black won." if status == -1 else " with a draw."
  if end is True: 
    print ( "Game has ended" + result )
    quit()
  print ( alphaBetaSearch(board, n, k, time) )
  
  
  
  
=======
import sys
import numpy as np
import copy
import heapq
from heapq import *

losing_seq = [ ]


def printable_board(board):
    return "\n".join([ " ".join(row) for row in board ])


def sequences(n, k):
    positions_groups = [ ]
    seq = (
        [ [ [ (x, y + z) for y in range(k) ] for z in range(n - k + 1) ] for x in range(n) ] +  # horizontals
        [ [ [ (x + z, y) for x in range(k) ] for z in range(n - k + 1) ] for y in range(n) ] +  # verticals
        [ [ [ (d + x, d + z) for d in range(k) ] for x in range(n - k + 1) ] for z in range(n - k + 1) ] +  # diag TL BR
        [ [ [ (n - 1 - d - x, d + z) for d in range(k) ] for x in range(n - k + 1) ] for z in range(n - k + 1) ]
    # diagonal BL TR
    )
    for s in seq:
        for d in s:
            positions_groups.append(d)
    return np.array(positions_groups)


def game_heuristic(board, n, k, seq):
    h = []
    empty_spot = zip(*np.where(board == '.'))
    white_pos = zip(*np.where(board == 'w'))
    blck_pos =  zip(*np.where(board == 'b'))

    if len(white_pos) >= len(blck_pos):
        for s in empty_spot:
            a1 = [ 1 for y in seq if ((y[ 0 ][ 0 ] == s or y[ 0 ][ 1 ] == s or y[ 0 ][ 2 ] == s) and y[ 0 ][ 0 ] != blck_pos and y[ 0 ][1 ] != blck_pos and y[ 0 ][ 2 ] != blck_pos) ]
            state_len = len(a1)
            heappush(h, (state_len, s))
            # need to mention return statement as return h but its throwing error , if you can place it with proper indentation
    else:
        for s in empty_spot:
            a1 = [ 1 for y in seq if ((y[ 0 ][ 0 ] == s or y[ 0 ][ 1 ] == s or y[ 0 ][ 2 ] == s) and y[ 0 ][ 0 ] != white_pos and y[ 0 ][1 ] != white_pos and y[ 0 ][ 2 ] != white_pos) ]
            state_len = len(a1)
            heappush(h, (state_len, s))




# Check whether game has ended and whether there is a tie, a win, or a lose
def game_status(board, n, k):
    for seq in losing_seq:
        vals = [ board[ x, y ] for [ x, y ] in seq ]
        if all(v == 'b' for v in vals): return True, 1
        if all(v == 'w' for v in vals): return True, -1
    if all('.' not in row for row in board): return True, 0
    return False, game_heuristic(board, n, k)


# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col, color):
    newboard = copy.deepcopy(board)
    newboard[ row, col ] = color
    return newboard


def successor(board, color):
    empty = zip(*np.where(board == '.'))
    return [ add_piece(board, row, col, color) for (row, col) in empty ]


# need to implement this
def branching_factor_function(time):
    return 20


def alphaBetaSearch(board, n, k, time):
    depth_limit = branching_factor_function(time)
    val, newboard = alphaBetaMinimax(board, n, k, -sys.maxsize, sys.maxsize, depth_limit, 0)
    return newboard


def alphaBetaMinimax(board, n, k, alpha, beta, depth_limit, depth):
    # check for leaf nodes
    end, status = game_status(board, n, k)
    if end is True: return status, board
    if depth >= depth_limit: return status, board
    # find whose turn it is
    color = 'b' if len(board[ board == 'w' ]) > len(board[ board == 'b' ]) else 'w'
    # get successors
    successors = successor(board, color)
    # keep track of best move
    best_move = board
    # if MAX's turn
    if color == 'w':
        for s in successors:
            result, newboard = alphaBetaMinimax(s, n, k, alpha, beta, depth_limit, depth + 1)
            if result > alpha:
                alpha = result
                best_move = s
            if alpha >= beta:
                break
        return alpha, best_move
    # if MIN's turn
    if color == 'b':
        for s in successors:
            result, newboard = alphaBetaMinimax(s, n, k, alpha, beta, depth_limit, depth + 1)
            if result < beta:
                beta = result
                best_move = s
            if beta <= alpha:
                break
        return beta, best_move


if "__main__" == __name__:
    n, k, board, time = int(sys.argv[ 1 ]), int(sys.argv[ 2 ]), str(sys.argv[ 3 ]), int(sys.argv[ 4 ])
    losing_seq = sequences(n, k)
    board = np.reshape(list(board), (n, n))
    print ("current board:")
    print (printable_board(board))
    end, status = game_status(board, n, k)
    result = ": white won." if status == 1 else ": black won." if status == -1 else " with a draw."
    if end is True:
        print ("Game has ended" + result)
        quit()
    print (alphaBetaSearch(board, n, k, time))
>>>>>>> bf7f633cc0f4fda9190d58761504d48c81de6139
