"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    player = 0
    for i in range(3):
        for j in range(3):
            state = board[i][j]
            if (state == X) or (state == O):
                player += 1
    if player % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3): 
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))  # Use .add() for a set
    return possible_actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    
    if(action not in actions(board)):
        raise Exception("Invalid action")
    
    auxBoard = copy.deepcopy(board)
    auxBoard[action[0]][action[1]] = player(board)
    return auxBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if board[0][0] == board[0][1] == board[0][2] != EMPTY:
        return board[0][0]
    if board[1][0] == board[1][1] == board[1][2] != EMPTY:
        return board[1][0]
    if board[2][0] == board[2][1] == board[2][2] != EMPTY:
        return board[2][0]
    if board[0][0] == board[1][0] == board[2][0] != EMPTY:
        return board[0][0]
    if board[0][1] == board[1][1] == board[2][1] != EMPTY:
        return board[0][1]
    if board[0][2] == board[1][2] == board[2][2] != EMPTY:
        return board[0][2]
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    winningGame = winner(board)
    if(winningGame != None):
        return True
    elif (winningGame == None ) and not any(EMPTY in tuple for tuple in board):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winningBoard = winner(board)
    if winningBoard == X:
        return 1
    elif winningBoard == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    action = set()
    
    if player(board) == X:
        bestValue = -2
        for a in actions(board):
            v = utility(result(board, a))
            if(v > bestValue):
                bestValue = v
                action = a
    else:
        bestValue = 2
        for a in actions(board):
            v = utility(result(board, a))
            if(v < bestValue):
                bestValue = v
                action = a
    return action
