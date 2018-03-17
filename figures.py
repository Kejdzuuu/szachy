import pygame

class ChessPiece:

    def __init__(self, x, y, board, color):
        self.x = x
        self.y = y
        self.board = board
        self.color = color

    def isLegal(self, new_x, new_y):
        return 0

    def move(self, new_x, new_y):

        if self.isLegal(new_x, new_y):
            self.x = new_x
            self.y = new_y


class Knight(ChessPiece):

    def isLegal(self, new_x, new_y):
        delta_x = new_x - self.x
        delta_y = new_y - self.y
        if abs(delta_x) == 1:
            if abs(delta_y) == 2:
                return True
        if abs(delta_y) == 1:
            if abs(delta_x) == 2:
                return True

        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_y, rect_x, self.board.grid_height/2, self.board.grid_width/2)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)