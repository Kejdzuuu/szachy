import pygame


class ChessPiece:

    def __init__(self, x, y, board, color, player):
        white = (0, 0, 0)
        black = (255, 255, 255)
        self.x = x
        self.y = y
        self.board = board
        self.player = player

        if color == "white":
            self.color = white
        else:
            self.color = black

        self.board.grid.append(self)
        self.player.figures.append(self)

    def is_legal(self, coords):
        return 0

    def try_move(self):
        if self.is_legal() is False:
            return False
        if self.is_occupied_by_friendly_figure() is True:
            return False
        if self.is_occupied_by_enemy() is not False:
            return True
        return True

    def is_occupied_by_friendly_figure(self):
        if self.player.get_figure(self.player.active_tile, self.player.figures) is False:
            return False
        else:
            return True

    def is_occupied_by_enemy(self):
        enemy_figures = self.player.game.get_enemy_figures(self.player.color)
        figure = self.player.get_figure(self.player.active_tile, enemy_figures)
        if figure is False:
            return False
        else:
            enemy = self.player.game.get_enemy(self.player.color)
            enemy.remove_figure(figure)
            return True

    def move(self):
        if self.try_move():
            self.x = self.player.active_tile[0]
            self.y = self.player.active_tile[1]
            return True
        else:
            return False


class Knight(ChessPiece):

    def is_legal(self):
        delta_x = self.player.active_tile[0] - self.x
        delta_y = self.player.active_tile[1] - self.y
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
        rect = (rect_x, rect_y, self.board.grid_width/2, self.board.grid_height/2)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)

class TheKing(ChessPiece):

    def is_legal(self):
        delta_x = self.player.active_tile[0] - self.x
        delta_y = self.player.active_tile[1] - self.y
        if abs(delta_x) <= 1 and abs(delta_y) <=1:
            return True
        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_x, rect_y, self.board.grid_width*2/3, self.board.grid_height*2/3)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)

class TheQueen(ChessPiece):

    def isLegal(self, new_x, new_y):
        delta_x = self.player.active_tile[0] - self.x
        delta_y = self.player.active_tile[1] - self.y
        if (not (abs(delta_x) == 0 and abs(delta_y) == 0)):
            if (abs(delta_x) == abs(delta_y)) or (abs(delta_x) == 0 and abs(delta_y) > 0) or (abs(delta_y) == 0 and abs(delta_x) > 0):
                return True
        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_x, rect_y, self.board.grid_width*2/3, self.board.grid_height/4)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)

class Rook(ChessPiece):

    def is_legal(self):
        delta_x = self.player.active_tile[0] - self.x
        delta_y = self.player.active_tile[1] - self.y
        if bool(delta_x) ^ bool(delta_y):
                return True
        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_y, rect_x, self.board.grid_height*2/3, self.board.grid_width*3/4)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)

class Bishop(ChessPiece):

    def is_legal(self):
        delta_x = self.player.active_tile[0] - self.x
        delta_y = self.player.active_tile[1] - self.y
        if abs(delta_x) > 0:
            if (abs(delta_x) == abs(delta_y)):
                return True
        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_y, rect_x, self.board.grid_height*2/3, self.board.grid_width*2/4)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)
