import tkinter as tk
from tkinter import messagebox
import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def initialize_board(size):
    return [[" " for _ in range(size)] for _ in range(size)]

def get_player_names():
    player1 = input("Enter name for Player 1 (X): ")
    player2 = input("Enter name for Player 2 (O): ")
    return player1, player2

def print_board_with_indices(board):
    print("   | " + " | ".join(str(i) for i in range(len(board))) + " |")
    print("-" * (4 * len(board) + 3))
    for i, row in enumerate(board):
        print(f" {i} | {' | '.join(row)} |")
        print("-" * (4 * len(board) + 3))

def check_winner(board, player, streak):
    def check_horizontal():
        for row in board:
            for i in range(len(row) - streak + 1):
                if all(cell == player for cell in row[i:i+streak]):
                    return True
        return False

    def check_vertical():
        for col in range(len(board)):
            for i in range(len(board) - streak + 1):
                if all(board[i + j][col] == player for j in range(streak)):
                    return True
        return False

    def check_diagonal():
        for i in range(len(board) - streak + 1):
            for j in range(len(board) - streak + 1):
                if all(board[i + k][j + k] == player for k in range(streak)):
                    return True
                if all(board[i + k][j + streak - 1 - k] == player for k in range(streak)):
                    return True
        return False

    return check_horizontal() or check_vertical() or check_diagonal()

def check_draw(board):
    return all(board[i][j] != " " for i in range(len(board)) for j in range(len(board)))

def is_valid_move(board, row, col):
    return 0 <= row < len(board) and 0 <= col < len(board) and board[row][col] == " "

def make_move(board, row, col, player):
    board[row][col] = player

def undo_move(board, row, col):
    board[row][col] = " "

def switch_player(current_player):
    return "X" if current_player == "O" else "O"

def get_computer_move(board, player, opponent, streak):
    best_score = float('-inf')
    best_move = None

    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                board[i][j] = player
                score = minimax(board, 0, False, player, opponent, streak)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move

def minimax(board, depth, maximizing_player, player, opponent, streak):
    if check_winner(board, player, streak):
        return 1
    if check_winner(board, opponent, streak):
        return -1
    if check_draw(board):
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == " ":
                    board[i][j] = player
                    eval = minimax(board, depth + 1, False, player, opponent, streak)
                    board[i][j] = " "
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == " ":
                    board[i][j] = opponent
                    eval = minimax(board, depth + 1, True, player, opponent, streak)
                    board[i][j] = " "
                    min_eval = min(min_eval, eval)
        return min_eval

def play_tic_tac_toe():
    size = int(input("Enter the board size (e.g., 3 for 3x3): "))
    player1, player2 = get_player_names()
    board = initialize_board(size)
    current_player = random.choice(["X", "O"])  # Randomly choose the starting player
    streak = size if size < 5 else 3  # The default winning streak will be 3 unless the size is greater than 5

    while True:
        print_board_with_indices(board)

        if current_player == "X" or current_player == player1:
            row, col = -1, -1
            while not is_valid_move(board, row, col):
                try:
                    row = int(input(f"{current_player}, enter row (0-{size-1}): "))
                    col = int(input(f"{current_player}, enter column (0-{size-1}): "))
                except ValueError:
                    print("Invalid input. Please enter a valid row and column.")
                    row, col = -1, -1
        else:
            # Computer's turn
            player = current_player
            opponent = player2 if player == player1 else player1
            row, col = get_computer_move(board, player, opponent, streak)
            print(f"{current_player} (Computer) chooses row {row} and column {col}.")

        make_move(board, row, col, current_player)
        if check_winner(board, current_player, streak):
            print_board(board)
            if current_player == "X":
                print(f"Congratulations! {player1} wins!")
            else:
                print(f"Congratulations! {player2} wins!")
            break
        elif check_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        else:
            current_player = switch_player(current_player)

if __name__ == "__main__":
    play_tic_tac_toe()
