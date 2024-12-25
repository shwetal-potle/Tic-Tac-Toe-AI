import tkinter as tk
import copy

# Define the main game class
class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = "X"  # Human player is X
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()
        self.window.mainloop()

    def create_board(self):
        for row in range(3):
            for col in range(3):
                self.buttons[row][col] = tk.Button(
                    self.window, text="", font=("Arial", 20), height=2, width=5,
                    command=lambda r=row, c=col: self.player_move(r, c)
                )
                self.buttons[row][col].grid(row=row, column=col)

    def player_move(self, row, col):
        if self.board[row][col] is None:
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player)
            if self.check_winner(self.current_player):
                self.end_game(f"Player {self.current_player} wins!")
            elif self.is_draw():
                self.end_game("It's a draw!")
            else:
                self.current_player = "O"  # Switch to AI
                self.ai_move()

    def ai_move(self):
        best_score = float('-inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    self.board[row][col] = "O"
                    score = self.minimax(self.board, 0, False)
                    self.board[row][col] = None
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        if best_move:
            row, col = best_move
            self.board[row][col] = "O"
            self.buttons[row][col].config(text="O")
            if self.check_winner("O"):
                self.end_game("AI wins!")
            elif self.is_draw():
                self.end_game("It's a draw!")
            else:
                self.current_player = "X"

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner("O"):
            return 10 - depth
        if self.check_winner("X"):
            return depth - 10
        if self.is_draw():
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] is None:
                        board[row][col] = "O"
                        score = self.minimax(board, depth + 1, False)
                        board[row][col] = None
                        best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for row in range(3):
                for col in range(3):
                    if board[row][col] is None:
                        board[row][col] = "X"
                        score = self.minimax(board, depth + 1, True)
                        board[row][col] = None
                        best_score = min(best_score, score)
            return best_score

    def check_winner(self, player):
        # Check rows, columns, and diagonals for a win
        for row in self.board:
            if all(s == player for s in row):
                return True
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True
        if all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def is_draw(self):
        return all(all(cell is not None for cell in row) for row in self.board)

    def end_game(self, message):
        for row in self.buttons:
            for button in row:
                button.config(state="disabled")
        tk.Label(self.window, text=message, font=("Arial", 16)).grid(row=3, column=0, columnspan=3)


# Run the game
if __name__ == "__main__":
    TicTacToe()
