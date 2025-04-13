def is_moves_left(board):
    return any(cell == "" for row in board for cell in row)

def evaluate(board):
    size = len(board)
    lines = []
    for i in range(size):
        lines.append([board[i][j] for j in range(size)])
        lines.append([board[j][i] for j in range(size)])
    lines.append([board[i][i] for i in range(size)])
    lines.append([board[i][size - i - 1] for i in range(size)])

    for line in lines:
        if line.count(line[0]) == size and line[0] != "":
            return 1 if line[0] == "O" else -1
    return 0

def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    if score in [1, -1]:
        return score
    if not is_moves_left(board):
        return 0

    size = len(board)
    if is_maximizing:
        best = -float('inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == "":
                    board[i][j] = "O"
                    best = max(best, minimax(board, depth + 1, False))
                    board[i][j] = ""
        return best
    else:
        best = float('inf')
        for i in range(size):
            for j in range(size):
                if board[i][j] == "":
                    board[i][j] = "X"
                    best = min(best, minimax(board, depth + 1, True))
                    board[i][j] = ""
        return best

def find_best_move(board):
    best_val = -float('inf')
    best_move = (-1, -1)
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == "":
                board[i][j] = "O"
                move_val = minimax(board, 0, False)
                board[i][j] = ""
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val
    return best_move

def ai_move(game, board):
    row, col = find_best_move(board)
    game.make_move(row, col)