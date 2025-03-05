from random import choice
from math import inf
from time import sleep

game_class = {
    'board': [[1, 2, 3],
             [4, 5, 6],
             [7, 8, 9]],
    'player': 'X',
    'opponent': 'O',
    'empty': ' ',
    'current_player': 'X',
    'winner': False,
    'full_board': False
}


def uvu():
    print("Welcome to the game of Tic-Tac-Toe!")
    sleep(1)
    print_gameboard(game_class)
    set_up(game_class)
    sleep(1)
    while (not game_class["winner"]) and not full_board(game_class):
        if game_class['current_player'] == 'X':
            print(f"The move of Player is {game_class['current_player']}")
            player_move(game_class)
            print_gameboard(game_class)
            if check_winner(game_class):
                game_class['winner'] = True
                break
        else:
            print(f"The move of Player is {game_class['current_player']}")
            ai_enhanced_move(game_class)
            sleep(1)
            print_gameboard(game_class)

            if check_winner(game_class):
                game_class['winner'] = True
                break
        game_class['current_player'] = 'X' if game_class['current_player'] == 'O' else 'O'    
    print_result(game_class)

def check_winner(game_class):
    if check_row(game_class['board'], game_class['current_player']) or check_col(game_class['board'], game_class['current_player']) or check_diago(game_class['board'], game_class['current_player']):
        game_class['winner'] = True
        return True
    
def full_board(game_class):
    empty = True
    for x, row in enumerate(game_class['board']):
        for y , _ in enumerate(row):
            if game_class["board"][x][y] == game_class['empty']:
                empty = False
    return empty

def player_move(game_class):
    valid_input = False
    while not valid_input:
        try:
            position = int(input("Enter the position For your move (1-9): "))
            if position >= 1 and position <= 9:
                row = (position - 1) // 3
                col = (position - 1) % 3
                if game_class["board"][row][col] == game_class['empty']:
                    game_class["board"][row][col] = game_class['current_player']
                    valid_input = True
                else:
                    print("Invalid move. The position is already occupied.")
            else:
                print("Invalid input. Please enter a number from 1 to 9.")
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 9.")

def print_result(game_class):
    if game_class['winner'] is True:
        print(f"The winner is {game_class['current_player']}")
    else:
        print("The game is a tie!")

def print_gameboard(game_class):
    print('==' * 10)

    print("The positions on the board are as follows: ")
    
    for row in game_class['board']:
        for pos in row:
            print(f'| {pos} ', end='')
        print('|\n' + '___' * 10)
    print("")
    print('==' * 10)
    print("")


def set_up(game_class):
    for x, row in enumerate(game_class['board']):
        for y, _ in enumerate(row):
            game_class['board'][x][y] = game_class['empty'] 

def check_row(board, player):
    for x, row in enumerate(board):
        win = True
        for y,_ in enumerate(row):
            if board[x][y] != player:
                win = False
                continue 
        if win == True:
            return(win)
    return(win)
 
 
 
def check_col(board, player):
    for x, row in enumerate(board):
        win = True
        for y,_ in enumerate(row):
            if board[y][x] != player:
                win = False
                continue
        if win == True:
            return(win)
    return(win)
 
# Checks whether the player has three
# of their marks in a diagonal row

 
def check_diago(board, player):
    win = True
    y = 0
    for x, _ in enumerate(board):
        if board[x][x] != player:
            win = False
    if win:
        return win
    win = True
    if win:
        for x, _ in enumerate(board):
            y = len(board) - 1 - x  
            if board[x][y] != player:
                win = False
    return win

def dfs_minimax(board,depth,maxi):
    # copy board to avoid modifying the original
    copy_board = [row[:] for row in board]
    #check  status
    if check_winner({'board': copy_board, 'current_player': 'O'}):
        return 10 - depth
    if check_winner({'board': copy_board, 'current_player': 'X'}):
        return -10 + depth
    if all(cell == ' ' for row in copy_board for cell in row):
        return 0
    # maximixing player 0
    if maxi:
        best_score = -inf
        for row in range(3):
            for col in range(3):
                if copy_board[row][col]== ' ':
                    copy_board[row][col]="X"
                    score = dfs_minimax(copy_board, depth+1, True)
                    #undo the move
                    copy_board[row][col]= ' '
                    best_score = max(best_score,score)
        return best_score

        # Minimizing player  X
    else:
        best_score = inf
        for row in range(3):
            for col in range(3):
                if copy_board[row][col] == ' ':
                    # Try this move
                    copy_board[row][col] = 'X'

                    # Recursive call
                    score = dfs_minimax(copy_board, depth + 1, True)

                    # Undo the move
                    copy_board[row][col] = ' '

                    best_score = min(best_score, score)
        return best_score


def ai_enhanced_move(game_class):
    best_score = -inf
    best_move = None

    for position in range(1, 10):
        row = (position - 1) // 3
        col = (position - 1) % 3

        # Check if empty
        if game_class['board'][row][col] == game_class['empty']:
            # Try move
            game_class['board'][row][col] = game_class['opponent']

            # Calculate the score using minimax with depth-first search
            score = dfs_minimax(game_class['board'], 0, False)

            # Undo the move
            game_class['board'][row][col] = game_class['empty']

            # Update best move
            if score > best_score:
                best_score = score
                best_move = position

    # Make the best move
    if best_move is not None:
        row = (best_move - 1) // 3
        col = (best_move - 1) % 3
        game_class['board'][row][col] = game_class['opponent']

uvu()

