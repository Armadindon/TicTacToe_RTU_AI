"""
Tic Tac Toe Player
"""

from queue import Empty
import random


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
    number_x = len(
        list(filter(lambda x: x == X, [element for row in board for element in row])))
    number_o = len(
        list(filter(lambda x: x == O, [element for row in board for element in row])))
    return X if (number_x - number_o) % 2 == 0 else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # Didn't know if i needed to return a set (the set object) or a list
    return [(i, j) for i in range(len(board)) for j in range(len(board)) if board[i][j] == EMPTY]


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    #We do a copy, for not having problems during the call on minimax algorithm
    boardCopy = [row.copy() for row in board].copy()
    boardCopy[action[0]][action[1]] = player(board)
    return boardCopy


def check_diagonal(board):
    """
    Utility function to check diagonals
    """
    # Get the two diagonal
    diagonal_1 = [board[i][i] for i in range(len(board))]
    diagonal_2 = [board[i][len(board) - 1 - i]
                  for i in range(len(board) - 1, -1, -1)]
    if all(list(map(lambda x: x == X, diagonal_1))) or all(list(map(lambda x: x == X, diagonal_2))):
        return X
    elif all(list(map(lambda x: x == O, diagonal_1))) or all(list(map(lambda x: x == O, diagonal_2))):
        return O
    else:
        return EMPTY


def check_line(board):
    """
    Utility function to check lines
    """
    # No need to do any transformation to get horizontal lines
    winning_horizontal_lines_x = [
        all(map(lambda x: x == X, line)) for line in board]
    winning_horizontal_lines_o = [
        all(map(lambda x: x == O, line)) for line in board]

    # apply transformation to get vertical as horizontal lines
    vertical_lines = [[board[j][i]
                       for j in range(len(board[i]))] for i in range(len(board))]
    winning_vertical_lines_x = [
        all(map(lambda x: x == X, row)) for row in vertical_lines]
    winning_vertical_lines_o = [
        all(map(lambda x: x == O, row)) for row in vertical_lines]

    return X if any(winning_horizontal_lines_x) or any(winning_vertical_lines_x) else (O if any(winning_horizontal_lines_o) or any(winning_vertical_lines_o) else EMPTY)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    result_line = check_line(board)
    if result_line != EMPTY:
        return result_line

    return check_diagonal(board)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return winner(board) != EMPTY or len(actions(board)) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    return 1 if win == X else (-1 if win == O else 0)

# alpha / beta are used for alpha beta pruning
def max_value(board, alpha, beta):
    """
    Function for the maximizing player
    """
    possible_actions = actions(board)

    if (terminal(board)):
        return utility(board)

    v = float('-inf')
    for action in possible_actions:
        value = min_value(result(board, action), alpha, beta)
        v = max(v, value)
        alpha = max(alpha, value)
        if beta <= alpha:
            break

    return v

# alpha / beta are used for alpha beta pruning
def min_value(board, alpha, beta):
    """
    Function for the minimizing player
    """
    possible_actions = actions(board)

    if (terminal(board)):
        return utility(board)

    v = float('inf')
    for action in possible_actions:
        value = max_value(result(board, action), alpha, beta)
        v = min(v, value)
        beta = min(beta, value)
        if beta <= alpha:
            break

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    possible_actions = actions(board)
    
    ai_player = player(board)
    weights = [max_value(result(board, action), float("-inf"), float("+inf")) for action in possible_actions] if ai_player == O else [
        min_value(result(board, action), float("-inf"), float("+inf")) for action in possible_actions]

    return possible_actions[min(range(len(weights)), key=weights.__getitem__) if ai_player == O else max(range(len(weights)), key=weights.__getitem__)]
