import pygame, os


class ChessPiece:

    def __init__(self, x, y, board, player):
        white = (0, 0, 0)
        black = (255, 255, 255)
        self.x = x
        self.y = y
        self.board = board
        self.player = player
        self.color = self.player.color
        self.first_move = 1
        self.srcname = ""
        self.image = self.load_image()
        self.board.grid.append(self)
        self.player.figures.append(self)

    def load_image(self):
        srcname = self.color + self.srcname
        image = pygame.image.load(os.path.join('szachy', 'img', srcname))
        image = pygame.transform.scale(image, (int(self.board.grid_width), int(self.board.grid_height)))
        return image

    def is_legal(self):
        return 0

    def try_move(self, coordinate):
        if self.is_legal(coordinate) is False:
            return False
        if self.is_occupied_by_friendly_figure(coordinate) is True:
            return False
        if self.is_occupied_by_enemy(coordinate) is not False:
            return True
        return True

    def is_occupied_by_friendly_figure(self, coordinate):
        if self.player.get_figure(coordinate, self.player.figures) is False:
            return False
        else:
            return True

    def is_occupied_by_enemy(self, coordinate):
        enemy_figures = self.player.game.get_enemy_figures(self.player.color)
        figure = self.player.get_figure(coordinate, enemy_figures)
        if figure is False:
            return False
        else:
            return True

    def move(self, coordinate):
        if self.try_move(coordinate):
            self.x = coordinate[0]
            self.y = coordinate[1]
            if self.is_occupied_by_enemy(coordinate) is True:
                enemy_figures = self.player.game.get_enemy_figures(self.player.color)
                figure = self.player.get_figure(coordinate, enemy_figures)
                enemy = self.player.game.get_enemy(self.player.color)
                enemy.remove_figure(figure)
            return True
        else:
            return False

    
class Knight(ChessPiece):
    def load_image(self):
        self.srcname = 'knight.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y
        if abs(delta_x) == 1:
            if abs(delta_y) == 2:
                return True
        if abs(delta_y) == 1:
            if abs(delta_x) == 2:
                return True
        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))


class TheKing(ChessPiece):

    def load_image(self):
        self.srcname = 'king.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y
        if abs(delta_x) <= 1 and abs(delta_y) <=1:
            return True
        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))


class TheQueen(ChessPiece):

    def load_image(self):
        self.srcname = 'queen.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y
        if (not (abs(delta_x) == 0 and abs(delta_y) == 0)):
            if (abs(delta_x) == abs(delta_y)) or (abs(delta_x) == 0 and abs(delta_y) > 0) or (abs(delta_y) == 0 and abs(delta_x) > 0):
                return True
        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))


class Rook(ChessPiece):

    def load_image(self):
        self.srcname = 'rook.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y
        if bool(delta_x) ^ bool(delta_y):
                return True
        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))


class Bishop(ChessPiece):

    def load_image(self):
        self.srcname = 'bishop.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y
        if abs(delta_x) > 0:
            if (abs(delta_x) == abs(delta_y)):
                return True
        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))


class Pawn(ChessPiece):

    def load_image(self):
        self.srcname = 'pawn.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y

        if self.color == "white":
            if delta_x == 0:
                if delta_y == 1 or (delta_y == 2 and self.first_move):
                    self.first_move = 0
                    return True
            if delta_y == 1 and abs(delta_x) == 1:
                if self.is_occupied_by_enemy(coordinate) is not False:
                    self.first_move = 0
                    return True
        else:
            if delta_x == 0:
                if delta_y == -1 or (delta_y == -2 and self.first_move):
                    self.first_move = 0
                    return True
            if delta_y == -1 and abs(delta_x) == 1:
                if self.is_occupied_by_enemy(coordinate) is not False:
                    self.first_move = 0
                    return True
        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))