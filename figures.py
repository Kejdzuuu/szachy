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
        self.image = self.load_image()
        self.board.grid.append(self)
        self.player.figures.append(self)

    def load_image(self, srcname):
        srcname = self.color + srcname
        image = pygame.image.load(os.path.join('szachy', 'img', srcname))
        image = pygame.transform.scale(image, (int(self.board.grid_width), int(self.board.grid_height)))
        return image

    def is_legal(self):
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
    srcname = 'knight.png'
    def load_image(self, srcname):
        return super().load_image(srcname)
    

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
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))



class TheKing(ChessPiece):
    srcname = 'king.png'
    def load_image(self, srcname):
        return super().load_image(srcname)

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
    srcname = 'queen.png'
    def load_image(self, srcname):
        return super().load_image(srcname)

    def is_legal(self):
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
    srcname = 'rook.png'
    def load_image(self, srcname):
        return super().load_image(srcname)

    def is_legal(self):
        delta_x = self.player.active_tile[0] - self.x
        delta_y = self.player.active_tile[1] - self.y
        if bool(delta_x) ^ bool(delta_y):
                return True
        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_x, rect_y, self.board.grid_width*2/3, self.board.grid_height*3/4)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)


class Bishop(ChessPiece):
    srcname = 'bishop.png'
    def load_image(self, srcname):
        return super().load_image(srcname)

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
        rect = (rect_x, rect_y, self.board.grid_width*2/3, self.board.grid_height*2/4)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)


class Pawn(ChessPiece):
    srcname = 'pawn.png'
    def load_image(self, srcname):
        return super().load_image(srcname)

    def is_legal(self):
        delta_x = self.player.active_tile[0] - self.x
        delta_y = self.player.active_tile[1] - self.y

        if self.color == "white":
            if delta_x == 0:
                if delta_y == 1 or (delta_y == 2 and self.first_move):
                    self.first_move = 0
                    return True
            if delta_y == 1 and abs(delta_x) == 1:
                if self.is_occupied_by_enemy() is not False:
                    self.first_move = 0
                    return True
        else:
            if delta_x == 0:
                if delta_y == -1 or (delta_y == -2 and self.first_move):
                    self.first_move = 0
                    return True
            if delta_y == -1 and abs(delta_x) == 1:
                if self.player.is_occupied_by_enemy is not False:
                    self.first_move = 0
                    return True
        return False

    def draw(self):
        rect_x = (self.x + 1 / 4) * self.board.grid_width
        rect_y = (self.y + 1 / 4) * self.board.grid_height
        rect = (rect_x, rect_y, self.board.grid_width*2/3, self.board.grid_height*2/4)
        pygame.draw.rect(self.board.screen, (0, 0, 0), rect)