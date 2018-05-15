import pygame, os


class ChessPiece:

    def __init__(self, x, y, board, player):
        white = (0, 0, 0)
        black = (255, 255, 255)
        self.score = 0
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
            last_coordinates = [self.x, self.y]
            self.x = coordinate[0]
            self.y = coordinate[1]
            if self.is_occupied_by_enemy(coordinate) is True:
                enemy_figures = self.player.game.get_enemy_figures(self.player.color)
                figure = self.player.get_figure(coordinate, enemy_figures)
                enemy = self.player.game.get_enemy(self.player.color)
                enemy.remove_figure(figure)
                self.player.moves_made.append([self, last_coordinates, figure, [figure.x, figure.y]])
            else:
                self.player.moves_made.append([self, last_coordinates, 0, 0])
            return True
        else:
            return False



    
class Knight(ChessPiece):
    def load_image(self):
        self.score = 30
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
        self.score = 900
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
        self.score = 90
        self.srcname = 'queen.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y
        
        if not (delta_x == 0 and delta_y == 0):
            if bool(delta_x) ^ bool(delta_y):
                if bool(delta_x):
                    delta = delta_x
                    index = 0
                elif bool(delta_y):
                    delta = delta_y
                    index = 1

                if(delta > 0):
                    sign = -1
                else:
                    sign = 1

                for i in range(1, abs(delta)):
                    coordinate[index] += sign * 1;

                    if (self.is_occupied_by_enemy(coordinate) or self.is_occupied_by_friendly_figure(coordinate)):
                        coordinate[index] -= sign * i
                        return False
                coordinate[index] -= sign * abs(delta) - sign
                return True

            elif abs(delta_x) > 0 and abs(delta_x) == abs(delta_y):
                if(delta_x > 0):
                    signx = -1
                else:
                    signx = 1

                if(delta_y > 0):
                    signy = -1
                else: 
                    signy = 1

                for i in range(1, abs(delta_x)):
                    coordinate[0] += signx * 1
                    coordinate[1] += signy * 1

                    if (self.is_occupied_by_enemy(coordinate) or self.is_occupied_by_friendly_figure(coordinate)):
                        coordinate[0] -= signx * i
                        coordinate[1] -= signy * i
                        return False
                coordinate[0] -= signx * abs(delta_x) - signx
                coordinate[1] -= signy * abs(delta_y) - signy
                return True

        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))


class Rook(ChessPiece):
    def load_image(self):
        self.score = 50
        self.srcname = 'rook.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y
        
        if bool(delta_x) ^ bool(delta_y):
            if bool(delta_x):
                delta = delta_x
                index = 0
            elif bool(delta_y):
                delta = delta_y
                index = 1

            if(delta > 0):
                sign = -1
            else:
                sign = 1

            for i in range(1, abs(delta)):
                coordinate[index] += sign * 1;

                if (self.is_occupied_by_enemy(coordinate) or self.is_occupied_by_friendly_figure(coordinate)):
                    coordinate[index] -= sign * i
                    return False
            coordinate[index] -= sign * abs(delta) - sign
            return True

        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))


class Bishop(ChessPiece):
    def load_image(self):
        self.score = 30
        self.srcname = 'bishop.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y
        
        if abs(delta_x) > 0 and abs(delta_x) == abs(delta_y):
            if(delta_x > 0):
                signx = -1
            else:
                signx = 1

            if(delta_y > 0):
                signy = -1
            else: 
                signy = 1

            for i in range(1, abs(delta_x)):
                coordinate[0] += signx * 1
                coordinate[1] += signy * 1

                if (self.is_occupied_by_enemy(coordinate) or self.is_occupied_by_friendly_figure(coordinate)):
                    coordinate[0] -= signx * i
                    coordinate[1] -= signy * i
                    return False
            coordinate[0] -= signx * abs(delta_x) - signx
            coordinate[1] -= signy * abs(delta_y) - signy
            return True

        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))


class Pawn(ChessPiece):
    def load_image(self):
        self.score = 10
        self.srcname = 'pawn.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y

        if self.color == "white":
            if delta_x == 0:
                if (delta_y == 1 or (delta_y == 2 and self.first_move)) and self.is_occupied_by_enemy(coordinate) is False:
                    self.first_move = 0
                    return True
            if delta_y == 1 and abs(delta_x) == 1:
                if self.is_occupied_by_enemy(coordinate) is not False:
                    self.first_move = 0
                    return True
        else:
            if delta_x == 0:
                if (delta_y == -1 or (delta_y == -2 and self.first_move)) and self.is_occupied_by_enemy(coordinate) is False:
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