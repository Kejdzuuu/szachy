import pygame, sys, os, time, random
import figures


class Game:

    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 800, 800
        self.screen = pygame.display.set_mode(self.size)
        color1 = (239, 235, 170)
        color2 = (135, 99, 1)
        self.board = ChessBoard(self.screen, self.width, self.height, color1, color2)
        self.player1 = Player(self.board, "white", self)
        self.player2 = AI(self.board, "black", self)
        self.queue = [self.player1, self.player2]
        self.counter = 0
        self.active_player = self.player1
        self.finished = False

    def take_turn(self):
        self.board.update(self.queue[self.counter].active_tile[0], self.queue[self.counter].active_tile[1], self.active_player.is_figure_selected)
        self.active_player.move()
        self.counter = (self.counter + 1) % 2
        self.active_player = self.queue[self.counter]

    def get_enemy_figures(self, color):
        if color == 'white':
            return self.queue[1].figures
        else:
            return self.queue[0].figures

    def get_enemy(self, color):
        if color == 'white':
            return self.queue[1]
        else:
            return self.queue[0]


class Player:

    def __init__(self, board, color, game):
        self.game = game
        self.color = color
        self.figures = []
        self.lost_figures = []
        self.board = board
        self.is_figure_selected = False
        self.selected_figure = 0
        self.moves_made = []
        if color is "white":
            self.active_tile = [0, 0]
            figures.Rook(0, 0, self.board, self)
            figures.Knight(1, 0, self.board, self)
            figures.Bishop(2, 0, self.board, self)
            figures.TheKing(3, 0, self.board, self)
            figures.TheQueen(4, 0, self.board, self)
            figures.Bishop(5, 0, self.board, self)
            figures.Knight(6, 0, self.board, self)
            figures.Rook(7, 0, self.board, self)
            for i in range(8):
                figures.Pawn(i, 1, self.board, self)
        else:
            self.active_tile = [0, 7]
            figures.Rook(0, 7, self.board, self)
            figures.Knight(1, 7, self.board, self)
            figures.Bishop(2, 7, self.board, self)
            figures.TheKing(3, 7, self.board, self)
            figures.TheQueen(4, 7, self.board, self)
            figures.Bishop(5, 7, self.board, self)
            figures.Knight(6, 7, self.board, self)
            figures.Rook(7, 7, self.board, self)
            for i in range(8):
                figures.Pawn(i, 6, self.board, self)

    def get_figure(self, active_tile, figures):
        for figure in figures:
            if figure.x == active_tile[0] and figure.y == active_tile[1]:
                return figure
        return False

    def remove_figure(self, figure):
        self.lost_figures.append(figure)
        self.figures.remove(figure)
        self.board.grid.remove(figure)
        if type(figure) is figures.TheKing:
            self.game.finished = True
            #self.board.update(0,0,False)


    def available_moves(self):
        moves = []
        for figure in self.figures:
            for x in range(self.board.boardSize):
                for y in range(self.board.boardSize):
                    if figure.try_move([x, y]) is True:
                        moves.append([figure, [x, y]])
        return moves

    def move(self):
        turn_finished = False

        while turn_finished is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if self.board.check_boundaries(self.active_tile[0] + 1) is True:
                            self.active_tile[0] += 1
                    if event.key == pygame.K_LEFT:
                        if self.board.check_boundaries(self.active_tile[0] - 1) is True:
                            self.active_tile[0] -= 1
                    if event.key == pygame.K_UP:
                        if self.board.check_boundaries(self.active_tile[1] - 1) is True:
                            self.active_tile[1] -= 1
                    if event.key == pygame.K_DOWN:
                        if self.board.check_boundaries(self.active_tile[1] + 1) is True:
                            self.active_tile[1] += 1
                    if event.key == pygame.K_RETURN:
                        if self.is_figure_selected is False:
                            self.is_figure_selected = True
                            self.selected_figure = self.get_figure(self.active_tile, self.figures)
                            if self.selected_figure is False:
                                self.is_figure_selected = False
                        elif self.is_figure_selected is True:
                            if self.selected_figure.move(self.active_tile) is True:
                                self.is_figure_selected = False
                                turn_finished = True
                            else:
                                self.is_figure_selected = False
                    if event.key == pygame.K_x:
                        self.undo_move()
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            self.board.update(self.active_tile[0], self.active_tile[1], self.is_figure_selected)

    def undo_move(self):
        figure = self.moves_made[-1][0]
        figure.x = self.moves_made[-1][1][0]
        figure.y = self.moves_made[-1][1][1]
        figure.moves_made -= 1
        if type(figure) is figures.Pawn:
            if self.color is 'white':
                if self.moves_made[-1][1][1] == 1:
                    self.moves_made[-1][0].first_move = 1
            else:
                if self.moves_made[-1][1][1] == 6:
                    self.moves_made[-1][0].first_move = 1
        if self.moves_made[-1][2] is not 0:
            self.insert_figure(self.moves_made[-1][2], self.moves_made[-1][3])
            #print(str(type(self)) + " " +str(type(self.moves_made[-1][2])) + "   " + str(self.moves_made[-1][3][0]) + " " + str(self.moves_made[-1][3][1]))
        self.moves_made.pop(-1)

    def insert_figure(self, figure, coords):
        x = coords[0]
        y = coords[1]
        enemy = self.game.get_enemy(self.color)
        for fig in enemy.lost_figures:
            if fig is figure:
                enemy.figures.append(fig)
                enemy.lost_figures.remove(fig)
                self.board.grid.append(fig)
                self.game.finished = False
                return

    def evaluate_board(self):
        evaluation = 0
        enemy_figures = self.game.get_enemy_figures(self.color)
        for figure in self.figures:
            evaluation += figure.score
        for figure in enemy_figures:
            evaluation += figure.score
        return -200

    def minimax(self, depth):
        best_move = -1
        best_value = -9999
        this_value = 0
        moves = self.available_moves()
        random.shuffle(moves)
        enemy = self.game.get_enemy(self.color)
        enemy_figures = game.get_enemy_figures(self.color)
        if len(moves) == 0:
            return [0, 0]
        for i in range(len(moves)):
            this_figure = moves[i][0]
            figure = self.get_figure(moves[i][1], enemy_figures)
            if figure is False:
                this_value = 0
                if this_figure.last_position == moves[i][1]:
                    if depth % 2 == 0:
                        this_value -= 100
            else:
                this_value = figure.score
                if type(figure) is figures.TheKing: ## nowe
                    return [i, this_value]
            if this_value < best_value:
                break
            this_figure.move(moves[i][1])
            if depth > 0:
                this_value = enemy.minimax(depth - 1)[1]
            self.undo_move()
            if this_value > best_value:
                best_value = this_value
                best_move = i
        return [best_move, best_value]

    def minimax_root(self, depth, is_maximising_player):
        moves = self.available_moves()
        best_value = -9999
        best_move = -1

        for i in range(len(moves)):
            this_figure = moves[i][0]
            this_figure.move(moves[i][1])
            value = self.minimax2(depth - 1, -10000, 10000, not is_maximising_player)
            self.undo_move()
            if value >= best_value:
                best_value = value
                best_move = i
        return best_move

    def minimax2(self, depth, alpha, beta, is_maximising_player):
        if depth is 0:
            return self.evaluate_board()

        moves = self.available_moves()
        if is_maximising_player is True:
            best_value = -9999
            for i in range(len(moves)):
                this_figure = moves[i][0]
                this_figure.move(moves[i][1])
                best_value = max(best_value, self.minimax2(depth - 1, alpha, beta, not is_maximising_player))
                self.undo_move()
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    return best_value
            return best_value
        else:
            best_value = 9999
            for i in range(len(moves)):
                this_figure = moves[i][0]
                this_figure.move(moves[i][1])
                best_value = min(best_value, self.minimax2(depth - 1, alpha, beta, not is_maximising_player))
                self.undo_move()
                beta = min(beta, best_value)
                if beta <= alpha:
                    return best_value
            return best_value


class AI(Player):

    def __init__(self, board, color, game):
        self.game = game
        self.color = color
        self.figures = []
        self.lost_figures = []
        self.board = board
        self.is_figure_selected = False
        self.active_tile = [0, 7]
        self.moves_made = []
        if color is "white":
            figures.Rook(0, 0, self.board, self)
            figures.Knight(1, 0, self.board, self)
            figures.Bishop(2, 0, self.board, self)
            figures.TheKing(3, 0, self.board, self)
            figures.TheQueen(4, 0, self.board, self)
            figures.Bishop(5, 0, self.board, self)
            figures.Knight(6, 0, self.board, self)
            figures.Rook(7, 0, self.board, self)
            for i in range(8):
                figures.Pawn(i, 1, self.board, self)
        else:
            figures.Rook(0, 7, self.board, self)
            figures.Knight(1, 7, self.board, self)
            figures.Bishop(2, 7, self.board, self)
            figures.TheKing(3, 7, self.board, self)
            figures.TheQueen(4, 7, self.board, self)
            figures.Bishop(5, 7, self.board, self)
            figures.Knight(6, 7, self.board, self)
            figures.Rook(7, 7, self.board, self)
            for i in range(8):
                figures.Pawn(i, 6, self.board, self)

    def move(self):
        moves = self.available_moves()
        best_move = self.minimax(2)
        moves[best_move[0]][0].move(moves[best_move[0]][1])
        # best_move = self.minimax_root(4, True)
        # moves[best_move][0].move(moves[best_move][1])


class ChessBoard:

    def __init__(self, screen, width, height, color1=(0, 0, 0), color2=(255, 255, 255)):
        self.height = height
        self.width = width
        self.boardSize = 8
        self.grid_height = self.height / self.boardSize
        self.grid_width = self.width / self.boardSize
        self.screen = screen
        self.colors = (color1, color2)
        self.grid = []

    def draw(self):
        rect_height = self.height / self.boardSize
        rect_width = self.width / self.boardSize
        for i in range(self.boardSize**2):
            rect = ((i % self.boardSize) * rect_width, int(i / self.boardSize) * rect_height, rect_width, rect_height)
            pygame.draw.rect(self.screen, self.colors[(i + int(i / self.boardSize)) % 2], rect)

    def pick_highlight_color(self, color_no):
        color_r = self.colors[color_no][0]
        if (color_r > 230):
            color_r -= 25
        else:
            color_r += 25

        color__g = self.colors[color_no][1]
        if (color__g > 230):
            color__g -= 25
        else:
            color__g += 25

        color__b = self.colors[color_no][2]
        if (color__b > 230):
            color__b -= 25
        else:
            color__b += 25

        color = (color_r, color__g, color__b)
        return color

    def active_tile(self, x, y):
        color = self.pick_highlight_color((x + y) % 2)
        rect_x = x * self.grid_width
        rect_y = y * self.grid_height
        rect = (rect_x, rect_y, self.grid_width, self.grid_height)
        pygame.draw.rect(self.screen, color, rect, 5)

    def highlight(self, x, y):
        color = (255,255,255)
        rect_x = x * self.grid_width
        rect_y = y * self.grid_height
        rect = (rect_x, rect_y, self.grid_width, self.grid_height)
        pygame.draw.rect(self.screen, color, rect)

    def update(self, x, y, is_selected):
        self.draw()
        self.active_tile(x, y)
        if is_selected is True:
            self.highlight(x, y)
        for figure in self.grid:
            figure.draw()
        pygame.display.flip()

    def check_boundaries(self, x):
        if x < 0:
            return False
        if x >= self.boardSize:
            return False
        return True


cwd = os.getcwd()
if cwd[-6:] == "szachy":
    cwd = cwd[0:-7]
    os.chdir(cwd)

game = Game()
move = [0,0]

while game.finished is False:
    start = time.time()
    game.take_turn()
    while (time.time() - start) < 1:
        time.sleep(0.1)

game.board.update(0, 0, False)
time.sleep(1)

white = (255, 255, 255)
black = (0, 0, 0)
block_width = 300
block_left = (game.width - block_width) / 2
block_height = 100
block_top = (game.height - block_height) / 2

pygame.draw.rect(game.screen, black, (block_left - 2, block_top - 2, block_width + 4, block_height + 4))
pygame.draw.rect(game.screen, white, (block_left, block_top, block_width, block_height))
myfont = pygame.font.SysFont("monospace", 30)
label = myfont.render("Szach i mat!", 1, (0, 0, 0))
game.screen.blit(label, (block_left + 50, block_top + 30))
pygame.display.flip()
pygame.display.update()
time.sleep(2)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            sys.exit()
