class TicTacToe:
    def __init__(self, size=3):
        self.size = size
        self.board = [["" for _ in range(size)] for _ in range(size)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.winning_line = None  # pour animation

    def make_move(self, row, col):
        if self.board[row][col] == "" and not self.game_over:
            self.board[row][col] = self.current_player
            self.check_winner()
            self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        lines = []
        # Rows and columns
        for i in range(self.size):
            lines.append([(i, j) for j in range(self.size)])
            lines.append([(j, i) for j in range(self.size)])
        # Diagonals
        lines.append([(i, i) for i in range(self.size)])
        lines.append([(i, self.size - i - 1) for i in range(self.size)])

        for line in lines:
            symbols = [self.board[i][j] for i, j in line]
            if symbols.count(symbols[0]) == self.size and symbols[0] != "":
                self.winner = symbols[0]
                self.winning_line = line
                self.game_over = True
                return

        if all(cell != "" for row in self.board for cell in row):
            self.winner = "Draw"
            self.game_over = True

    def reset(self):
        self.__init__(self.size)

    def set_size(self, new_size):
        self.__init__(new_size)

    def get_winning_line(self):
        return self.winning_line if self.game_over and self.winner != "Draw" else None

    def get_board(self):
        return self.board