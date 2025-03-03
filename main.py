import tkinter as tk
from tkinter import messagebox

game_class = {
    'board': [[' ' for _ in range(3)] for _ in range(3)],
    'player': 'X',
    'opponent': 'O',
    'current_player': 'X',
    'winner': False
}

# Function to handle player moves
def player_move(row, col):
    if game_class["board"][row][col] == ' ' and not game_class["winner"]:
        game_class["board"][row][col] = game_class["current_player"]
        buttons[row][col].config(text=game_class["current_player"])

        if check_winner():
            messagebox.showinfo("Game Over", f"Player {game_class['current_player']} wins!")
            game_class["winner"] = True
        elif full_board():
            messagebox.showinfo("Game Over", "It's a Tie!")
            game_class["winner"] = True
        else:
            game_class["current_player"] = 'X' if game_class["current_player"] == 'O' else 'O'

# Function to check for a winner
def check_winner():
    board = game_class['board']
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return True
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return True
    if board[0][0] == board[1][1] == board[2][2] != ' ' or board[0][2] == board[1][1] == board[2][0] != ' ':
        return True
    return False

# Function to check if the board is full
def full_board():
    return all(cell != ' ' for row in game_class["board"] for cell in row)

# Create the GUI window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create a 3x3 grid of buttons
buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=" ", font=("Arial", 24), width=5, height=2,
                                  command=lambda row=i, col=j: player_move(row, col))
        buttons[i][j].grid(row=i, column=j)

root.mainloop()
