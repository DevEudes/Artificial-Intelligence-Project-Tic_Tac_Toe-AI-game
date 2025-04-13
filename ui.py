import pygame
from game import TicTacToe
from ai import find_best_move

WIDTH = 600
HEIGHT = 700
WHITE = (245, 245, 245)
BLACK = (33, 33, 33)
PRIMARY = (66, 133, 244)
ACCENT = (219, 68, 55)
GREEN = (52, 168, 83)
LINE_WIDTH = 6

class GameUI:
    def __init__(self):
        self.grid_size = 3
        self.cell_size = 140
        self.board_size = self.cell_size * self.grid_size

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tic Tac Toe AI")
        self.clock = pygame.time.Clock()
        self.game = TicTacToe(self.grid_size)
        self.font = pygame.font.SysFont("Segoe UI", 64, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI", 28)
        self.symbol = None

    def draw_board(self):
        self.screen.fill(WHITE)
        offset_x = (WIDTH - self.board_size) // 2
        offset_y = 60

        for i in range(1, self.grid_size):
            pygame.draw.line(self.screen, PRIMARY, (offset_x, offset_y + i * self.cell_size), (offset_x + self.board_size, offset_y + i * self.cell_size), LINE_WIDTH)
            pygame.draw.line(self.screen, PRIMARY, (offset_x + i * self.cell_size, offset_y), (offset_x + i * self.cell_size, offset_y + self.board_size), LINE_WIDTH)

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                symbol = self.game.board[i][j]
                if symbol:
                    color = BLACK if symbol == "X" else ACCENT
                    img = self.font.render(symbol, True, color)
                    rect = img.get_rect(center=(offset_x + j * self.cell_size + self.cell_size // 2, offset_y + i * self.cell_size + self.cell_size // 2))
                    self.screen.blit(img, rect)

        if self.game.game_over:
            pygame.draw.rect(self.screen, PRIMARY, (0, HEIGHT - 200, WIDTH, 200))
            msg = "Draw!" if self.game.winner == "Draw" else f"{self.game.winner} wins!"
            text = self.font.render(msg, True, WHITE)
            self.screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 180))

            pygame.draw.rect(self.screen, WHITE, (WIDTH // 2 - 120, HEIGHT - 100, 240, 40), border_radius=10)
            restart_text = self.small_font.render("Play Again", True, GREEN)
            self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT - 100))

            pygame.draw.rect(self.screen, WHITE, (WIDTH // 2 - 120, HEIGHT - 40, 240, 40), border_radius=10)
            home_text = self.small_font.render("Back to Home", True, ACCENT)
            self.screen.blit(home_text, (WIDTH // 2 - home_text.get_width() // 2, HEIGHT - 40))

            line = self.game.get_winning_line()
            if line:
                i1, j1 = line[0]
                i2, j2 = line[-1]
                x1 = offset_x + j1 * self.cell_size + self.cell_size // 2
                y1 = offset_y + i1 * self.cell_size + self.cell_size // 2
                x2 = offset_x + j2 * self.cell_size + self.cell_size // 2
                y2 = offset_y + i2 * self.cell_size + self.cell_size // 2
                pygame.draw.line(self.screen, GREEN, (x1, y1), (x2, y2), 8)

    def handle_click(self, pos):
        if self.game.game_over:
            if HEIGHT - 80 <= pos[1] <= HEIGHT - 40:
                self.game.reset()
                if self.symbol == "O":
                    ai_move = find_best_move(self.game.board)
                    self.game.make_move(*ai_move)
                return
            elif HEIGHT - 40 <= pos[1] <= HEIGHT:
                self.symbol = None
                self.game.reset()
                return

        offset_x = (WIDTH - self.board_size) // 2
        offset_y = 60

        if pos[1] > offset_y + self.board_size:
            return

        col = (pos[0] - offset_x) // self.cell_size
        row = (pos[1] - offset_y) // self.cell_size
        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            if self.game.board[row][col] == "" and self.game.current_player == self.symbol:
                self.game.make_move(row, col)
                if not self.game.game_over:
                    ai_move = find_best_move(self.game.board)
                    self.game.make_move(*ai_move)

    def draw_start_screen(self):
        self.screen.fill(WHITE)
        title = self.font.render("Tic Tac Toe AI", True, PRIMARY)
        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 80))

        pygame.draw.circle(self.screen, ACCENT, (WIDTH // 2, 250), 50, 5)
        pygame.draw.line(self.screen, PRIMARY, (WIDTH // 2 - 30, 280), (WIDTH // 2 + 30, 220), 5)
        pygame.draw.line(self.screen, PRIMARY, (WIDTH // 2 + 30, 280), (WIDTH // 2 - 30, 220), 5)

        prompt = self.font.render("Choose X or O", True, BLACK)
        self.screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 300))

        pygame.draw.rect(self.screen, PRIMARY, (150, 400, 100, 100), border_radius=20)
        pygame.draw.rect(self.screen, ACCENT, (350, 400, 100, 100), border_radius=20)

        x_text = self.font.render("X", True, WHITE)
        o_text = self.font.render("O", True, WHITE)
        self.screen.blit(x_text, (200 - x_text.get_width() // 2, 450 - x_text.get_height() // 2))
        self.screen.blit(o_text, (400 - o_text.get_width() // 2, 450 - o_text.get_height() // 2))

    def run(self):
        while True:
            if not self.symbol:
                choosing = True
                while choosing:
                    self.draw_start_screen()
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            x, y = event.pos
                            if 150 <= x <= 250 and 360 <= y <= 460:
                                self.symbol = "X"
                                choosing = False
                            elif 350 <= x <= 450 and 360 <= y <= 460:
                                self.symbol = "O"
                                choosing = False

                self.game = TicTacToe(self.grid_size)
                if self.symbol == "O":
                    ai_move = find_best_move(self.game.board)
                    self.game.make_move(*ai_move)

            self.draw_board()
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
            self.clock.tick(60)
