import pygame, sys
import figures

class Game:

    def __init__(self):
        player1 = Player("white")
        player2 = Player("black")
        self.queue = [player1, player2]
        self.counter = 0

    def takeTurn(self):
        self.queue[self.counter].move()
        self.counter = (self.counter + 1) % 2


class Player:

    def __init__(self, color):
        self.color = color
        self.figures = []
        # figures.Knight(2,2, board, "white", )


    def move(self):
        return 0

class ChessBoard:

    def __init__(self, screen, height: object, width: object, color1: object = (0, 0, 0), color2: object = (255, 255, 255)) -> object:
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
            rect = ((i % self.boardSize) * rect_height, int(i / self.boardSize) * rect_width, rect_height, rect_width)
            pygame.draw.rect(screen, self.colors[(i + int(i / self.boardSize)) % 2], rect)

    def pickHighlightColor(self, color_no):
        color_R = self.colors[color_no][0]
        if (color_R > 250):
            color_R -= 5
        else:
            color_R += 5

        color_G = self.colors[color_no][1]
        if (color_G > 250):
            color_G -= 5
        else:
            color_G += 5

        color_B = self.colors[color_no][1]
        if (color_B > 250):
            color_B -= 5
        else:
            color_B += 5

        color = (color_R, color_G, color_B)
        return color

    def highlight(self, x, y):
        color = self.pickHighlightColor((x + y) % 2)
        rect_x = x * self.grid_width
        rect_y = y * self.grid_height
        rect = (rect_y, rect_x, self.grid_height, self.grid_width)
        pygame.draw.rect(screen, color, rect)






color1 = (239, 235, 170)
color2 = (135, 99, 1)

pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
board = ChessBoard(screen, width, height, color1, color2)
knight = figures.Knight(2, 2, board, "white")
move = [0,0]

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move[1] += 1
            if event.key == pygame.K_LEFT:
                move[1] -= 1
            if event.key == pygame.K_UP:
                move[0] -= 1
            if event.key == pygame.K_DOWN:
                move[0] += 1
            if event.key == pygame.K_RETURN:
                knight.move(move[0], move[1])
            if event.key == pygame.K_ESCAPE:
                sys.exit()


    board.draw()
    board.highlight(move[0], move[1])
    knight.draw()


    pygame.display.flip()
