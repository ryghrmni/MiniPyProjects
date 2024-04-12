import tkinter as tk
from tkinter import messagebox

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        self.current_player = "X"
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(root, text="", font=("Helvetica", 20), width=5, height=2,
                                                   command=lambda r=row, c=col: self.make_move(r, c))
                self.buttons[row][col].grid(row=row, column=col)

        self.reset_button = tk.Button(root, text="New Game", command=self.reset_game)
        self.reset_button.grid(row=3, column=0, columnspan=3)

    def make_move(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)

            if self.check_winner(row, col):
                messagebox.showinfo("Winner!", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Draw!", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = "X" if self.current_player == "O" else "O"

    def check_winner(self, row, col):
        symbol = self.board[row][col]

        # Check the row and column
        if all(self.board[row][c] == symbol for c in range(3)) or all(self.board[r][col] == symbol for r in range(3)):
            return True

        # Check diagonals
        if row == col and all(self.board[i][i] == symbol for i in range(3)):
            return True
        if row + col == 2 and all(self.board[i][2-i] == symbol for i in range(3)):
            return True

        return False

    def check_draw(self):
        return all(self.board[row][col] != ' ' for row in range(3) for col in range(3))

    def reset_game(self):
        self.current_player = "X"
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text="")
    
# Create the main window
root = tk.Tk()
game = TicTacToeGame(root)
root.mainloop()
