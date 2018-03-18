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

    def is_legal(self, new_x, new_y):
        return 0

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


    def move(self, new_x, new_y):

        if self.is_legal(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        else:
            return False


class Knight(ChessPiece):

    def is_legal(self, new_x, new_y):
        delta_x = new_x - self.x
        delta_y = new_y - self.y
        check = True
        if self.is_occupied_by_friendly_figure() is True:
            return False
        if abs(delta_x) == 1:
            if abs(delta_y) == 2:
                check = True
        if abs(delta_y) == 1:
            if abs(delta_x) == 2:
                check = True
        if check is True:
            if self.is_occupied_by_enemy() is not False:
                return True
        return check

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_x, rect_y, self.board.grid_width/2, self.board.grid_height/2)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)

class TheKing(ChessPiece):

    def is_legal(self, new_x, new_y):
        delta_x = new_x - self.x
        delta_y = new_y - self.y
        if self.is_occupied_by_friendly_figure() is True:
            return False
        if abs(delta_x) <= 1 and abs(delta_y) <=1:
            if self.is_occupied_by_enemy() is not False:
                return True
            return True
        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_x, rect_y, self.board.grid_width*2/3, self.board.grid_height*2/3)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)

class TheQueen(ChessPiece):

    def isLegal(self, new_x, new_y):
        delta_x = new_x - self.x
        delta_y = new_y - self.y
        if (not (abs(delta_x) == 0 and abs(delta_y) == 0)):
            if (abs(delta_x) == abs(delta_y)) or (abs(delta_x) == 0 and abs(delta_y) > 0) or (abs(delta_y) == 0 and abs(delta_x) > 0):
                return True
        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_x, rect_y, self.board.grid_width*2/3, self.board.grid_height/4)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)