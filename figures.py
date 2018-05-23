import pygame, os, time


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
        self.moves_made = 0
        self.srcname = ""
        self.image = self.load_image()
        self.board.grid.append(self)
        self.player.figures.append(self)
        self.last_position = []
        self.evaluation_board = []

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
            self.moves_made += 1
            last_coordinates = [self.x, self.y]
            self.last_position = last_coordinates
            self.x = coordinate[0]
            self.y = coordinate[1]
            if self.is_occupied_by_enemy(coordinate) is True:
                enemy_figures = self.player.game.get_enemy_figures(self.player.color)
                figure = self.player.get_figure(coordinate, enemy_figures)
                enemy = self.player.game.get_enemy(self.player.color)
                self.player.moves_made.append([self, last_coordinates, figure, [figure.x, figure.y]])
                enemy.remove_figure(figure)
            else:
                self.player.moves_made.append([self, last_coordinates, 0, 0])
            return True
        else:
            return False


class Knight(ChessPiece):
    def __init__(self, x, y, board, player):
        super().__init__(x, y, board, player)
        self.evaluation_board = [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
            [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
            [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
            [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
            [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
            [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]
        self.score = 30
        if self.color is "black":
            self.score *= -1

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
    def __init__(self, x, y, board, player):
        super().__init__(x, y, board, player)
        self.evaluation_board = [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
            [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]]
        self.score = 900
        if self.color is "black":
            self.score *= -1
            self.evaluation_board.reverse()

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
    def __init__(self, x, y, board, player):
        super().__init__(x, y, board, player)
        self.evaluation_board = [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]
        self.score = 90
        if self.color is "black":
            self.score *= -1

    def load_image(self):
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
    def __init__(self, x, y, board, player):
        super().__init__(x, y, board, player)
        self.evaluation_board = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]]
        self.score = 50
        if self.color is "black":
            self.score *= -1
            self.evaluation_board.reverse()

    def load_image(self):
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
    def __init__(self, x, y, board, player):
        super().__init__(x, y, board, player)
        self.evaluation_board = [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
            [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
            [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
            [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]
        self.score = 30
        if self.color is "black":
            self.score *= -1
            self.evaluation_board.reverse()

    def load_image(self):
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
    def __init__(self, x, y, board, player):
        super().__init__(x, y, board, player)
        self.evaluation_board = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
        self.score = 10
        if self.color is "black":
            self.score *= -1
            self.evaluation_board.reverse()

    def load_image(self):
        self.srcname = 'pawn.png'
        return super().load_image()

    def is_legal(self, coordinate):
        delta_x = coordinate[0] - self.x
        delta_y = coordinate[1] - self.y

        if self.color == "white":
            if delta_x == 0:
                if (delta_y == 1 or (delta_y == 2 and self.moves_made == 0)) and self.is_occupied_by_enemy(coordinate) is False:
                    return True
            if delta_y == 1 and abs(delta_x) == 1:
                if self.is_occupied_by_enemy(coordinate) is not False:
                    return True
        else:
            if delta_x == 0:
                if (delta_y == -1 or (delta_y == -2 and self.moves_made == 0)) and self.is_occupied_by_enemy(coordinate) is False:
                    return True
            if delta_y == -1 and abs(delta_x) == 1:
                if self.is_occupied_by_enemy(coordinate) is not False:
                    return True
        return False

    def draw(self):
        rect_x = self.x * self.board.grid_width
        rect_y = self.y * self.board.grid_height
        self.board.screen.blit(self.image, (rect_x, rect_y))