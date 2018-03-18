import pygame, sys
import figures


class Game:

    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size)
        color1 = (239, 235, 170)
        color2 = (135, 99, 1)
        self.board = ChessBoard(self.screen, self.width, self.height, color1, color2)
        player1 = Player(self.board, "white")
        player2 = Player(self.board, "black")
        self.queue = [player1, player2]
        self.counter = 0
        self.active_player = player1

    def take_turn(self):
        self.board.update(self.queue[self.counter].active_tile[0], self.queue[self.counter].active_tile[1], self.active_player.is_figure_selected)
        self.active_player.move()
        self.counter = (self.counter + 1) % 2
        self.active_player = self.queue[self.counter]

class Player:

    def __init__(self, board, color):
        self.color = color
        self.figures = []
        self.board = board
        self.is_figure_selected = False
        self.selected_figure = 0
        if color is "white":
            self.active_tile = [0, 0]

            figures.Knight(0, 0, self.board, self.color, self)
            figures.TheKing(1, 0, self.board, self.color, self)
        else:
            self.active_tile = [0, 7]

            figures.Knight(0, 7, self.board, self.color, self)
            figures.TheKing(1, 7, self.board, self.color, self)

    def get_figure(self, active_tile):
        for figure in self.figures:
            if figure.x == active_tile[0] and figure.y == active_tile[1]:
                return figure

        return 0

    def move(self):
        turn_finished = False

        while turn_finished is False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.active_tile[0] += 1
                    if event.key == pygame.K_LEFT:
                        self.active_tile[0] -= 1
                    if event.key == pygame.K_UP:
                        self.active_tile[1] -= 1
                    if event.key == pygame.K_DOWN:
                        self.active_tile[1] += 1
                    if event.key == pygame.K_RETURN:
                        if self.is_figure_selected is False:
                            self.is_figure_selected = True
                            self.selected_figure = self.get_figure(self.active_tile)
                            if self.selected_figure == 0:
                                self.is_figure_selected = False
                        elif self.is_figure_selected is True:
                            if self.selected_figure.move(self.active_tile[0], self.active_tile[1]) is True:
                                self.is_figure_selected = False
                                turn_finished = True

                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

            self.board.update(self.active_tile[0], self.active_tile[1], self.is_figure_selected)



class ChessBoard:

    def __init__(self, screen, width, height, color1 = (0, 0, 0), color2 = (255, 255, 255)):
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
        print(x, y)
        pygame.draw.rect(self.screen, color, rect)

    def highlight(self, x, y):
        color = (255,255,255)
        rect_x = x * self.grid_width
        rect_y = y * self.grid_height
        rect = (rect_x, rect_y, self.grid_width, self.grid_height)
        print(x, y)
        pygame.draw.rect(self.screen, color, rect)

    def update(self, x, y, is_selected):
        self.draw()
        self.active_tile(x, y)
        if is_selected is True:
            self.highlight(x, y)
        for figure in self.grid:
            figure.draw()

        pygame.display.flip()



game = Game()
move = [0,0]

while True:
    game.take_turn()



