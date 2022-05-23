import random
import copy

field_0 = [["  |", "1 |", "2 |", "3 |", "4 |", "5 |", "6 |\n"],
           ["1 |", "O |", "O |", "O |", "O |", "O |", "O |\n"],
           ["2 |", "O |", "O |", "O |", "O |", "O |", "O |\n"],
           ["3 |", "O |", "O |", "O |", "O |", "O |", "O |\n"],
           ["4 |", "O |", "O |", "O |", "O |", "O |", "O |\n"],
           ["5 |", "O |", "O |", "O |", "O |", "O |", "O |\n"],
           ["6 |", "O |", "O |", "O |", "O |", "O |", "O |\n"]]


# Inner logic


class BoardOutException(Exception):
    pass


class ShipPositionException(Exception):
    pass


class DoubleShotException(Exception):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"{self.x}, {self.y}"

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if type(value) == int:
            self._x = value
        else:
            raise ValueError

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if type(value) == int:
            self._y = value
        else:
            raise ValueError


class Ship:
    def __init__(self, length, bow, direction, hp):
        self.length = length
        self.bow = bow
        self.direction = direction
        self.hp = hp

    def dots(self):
        ship_dots = []
        if self.direction == "v":
            ship_dots = [Dot(self.bow.x, self.bow.y + i) for i in range(self.length)]
        elif self.direction == "h":
            ship_dots = [Dot(self.bow.x + i, self.bow.y) for i in range(self.length)]
        return ship_dots


class Board:
    def __init__(self, cells=None, ships=None, hid=False, active_ships=0):
        if ships is None:
            ships = []
        if cells is None:
            cells = copy.deepcopy(field_0)
        self.cells = cells
        self.ships = ships
        self.hid = hid
        self.active_ships = active_ships

    def add_ship(self, ship):
        if any([
            ship.length == 3 and (ship.bow.x > 4 or ship.bow.y > 4),
            ship.length == 2 and (ship.bow.x > 5 or ship.bow.y > 5)
        ]):
            raise ShipPositionException
        else:
            for dot in ship.dots():
                for other_ship in self.ships:
                    if any([
                        dot in other_ship.dots(),
                        dot in self.contour(other_ship),
                    ]):
                        raise ShipPositionException
                self.cells[dot.y][dot.x] = "■" + self.cells[dot.y][dot.x][1:]
        self.ships.append(ship)

    def contour(self, ship):
        contour_cells = []
        for dot in ship.dots():
            for i in range(-1, 2):
                for j in range(-1, 2):
                    cell = Dot(dot.x + i, dot.y + j)
                    if all([
                        not self.out(cell),
                        cell not in contour_cells,
                        cell not in ship.dots()
                    ]):
                        contour_cells.append(cell)
        return contour_cells

    def print_board(self):
        visible_board = "".join(list(map(" ".join, self.cells)))
        if self.hid:
            print(visible_board.replace("■", "O"))
        else:
            print(visible_board)

    @staticmethod
    def out(dot):
        if any([
            dot.x < 1,
            dot.x > 6,
            dot.y < 1,
            dot.y > 6
        ]):
            return True
        return False

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException
        if self.cells[dot.y][dot.x][0] == "T" or self.cells[dot.y][dot.x][0] == "X":
            raise DoubleShotException
        elif self.cells[dot.y][dot.x][0] == "■":
            self.cells[dot.y][dot.x] = "X" + self.cells[dot.y][dot.x][1:]
            for ship in self.ships:
                if Dot(dot.x, dot.y) in ship.dots():
                    ship.hp -= 1
                    print("Ранен!")
                    if ship.hp == 0:
                        for dot in self.contour(ship):
                            self.cells[dot.y][dot.x] = "T" + self.cells[dot.y][dot.x][1:]
                        self.ships.remove(ship)
                        self.active_ships -= 1
                        print("Убит! Осталось кораблей:", self.active_ships)
        else:
            self.cells[dot.y][dot.x] = "T" + self.cells[dot.y][dot.x][1:]
            print("Мимо!")


# Outer logic


class Player:
    def __init__(self, their_board=None, enemy_board=None):
        self.their_board = their_board
        self.enemy_board = enemy_board

    def ask(self):
        pass

    def move(self):
        target = self.ask()
        try:
            self.enemy_board.shot(target)
        except BoardOutException:
            print("Нельзя стрелять за пределы поля!")
            return True
        except DoubleShotException:
            print("Нельзя стрелять по одной клетке дважды!")
            return True
        if self.enemy_board.cells[target.y][target.x][0] == "X":
            return True
        return False


class AI(Player):
    def ask(self):
        return Dot(random.randint(1, 6), random.randint(1, 6))


class User(Player):
    def ask(self):
        while True:
            try:
                target = Dot(int(input("Введите координату x: ")), int(input("Введите координату y: ")))
            except ValueError:
                print("Координата должна быть целым числом!")
            else:
                return target


class Game:
    def __init__(self, user=User(), user_board=None, computer=AI(), computer_board=None):
        self.user = user
        self.user_board = user_board
        self.computer = computer
        self.computer_board = computer_board

    @staticmethod
    def random_board(board):
        global field_0
        board.add_ship(
            Ship(3, Dot(random.randint(1, 4), random.randint(1, 4)), random.choice(["h", "v"]), 3)
        )
        for n in range(2):
            while True:
                try:
                    board.add_ship(
                        Ship(2, Dot(random.randint(1, 5), random.randint(1, 5)), random.choice(["h", "v"]), 2)
                    )
                except ShipPositionException:
                    pass
                else:
                    break
        for n in range(4):
            attempts = 0
            while True:
                try:
                    board.add_ship(
                        Ship(1, Dot(random.randint(1, 6), random.randint(1, 6)), random.choice(["h", "v"]), 1)
                    )
                except ShipPositionException:
                    attempts += 1
                else:
                    break
                if attempts == 2000:
                    board.cells = copy.deepcopy(field_0)
                    board.ships = []
                    break
            if board.cells == field_0:
                break

    # Примечание: данный метод понадобился по причине того, что random_board при запуске создавал доски с "мнимыми"
    # точками. На поле появлялись ячейки, отображающие палубы, хотя их как объектов там не было (т. е. атрибуты
    # self.dots экземпляров класса Ship не содержали объектов класса Dot с соответствующими координатами), а найти
    # ошибку так и не удалось
    def board_check(self, board):
        while not len(board.ships) == 7:
            self.random_board(board)
        board.active_ships = 7
        total_ship_dots = []
        for ship in board.ships:
            for dot in ship.dots():
                total_ship_dots.append(dot)
        for i, k in enumerate(board.cells):
            for j, m in enumerate(k):
                if m[0] == "■":
                    if not Dot(j, i) in total_ship_dots:
                        k[j] = k[j].replace("■", "O")
        return board

    @staticmethod
    def greet():
        print("Приветствуем вас в игре 'Морской Бой!'\n"
              "Вам, Игроку, предстоит сразиться с Компьютером\n"
              "Правила:\n"
              "- Поле представляет собой доску 6x6, на которой случайным образом создаются корабли\n"
              "- Всего их 7: 1 трёхпалубный крейсер, 2 двухпалубных эсминца и 4 однопалубных торпедных катера\n"
              "- Располагаются на доске они таким образом, чтобы никак не касаться друг друга\n"
              "- Вам доступно 2 поля: первое - с вашими кораблями, второе - с кораблями противника (скрытыми)\n"
              "- Ваша цель - потопить все корабли противника\n"
              "- Чтобы выстрелить, вам надо поочерёдно ввести координаты по горизонтали (x) и вертикали (y)\n"
              "- Если вам удасться нанести удар по вражескому кораблю, вам будет дан ещё один ход\n"
              "- Если промажете, то ход перейдёт к Компьютеру, который действует по тем же правилам\n"
              "- Стрелять можно только по клеткам внутри поля и только один раз по одной клетке!\n"
              "- Но не переживайте! Если вы введёте неправильные координаты, вы сможете выстрелить ещё раз\n"
              "- Если сможете потопить корабль, окружающие клетки будут автоматически помечены\n"
              "- Как только последний вражеский (или же ваш) корабль потонет, игра будет завершена")

    def loop(self):
        user_flag = True
        computer_flag = False
        winner_flag = ""
        self.user_board.print_board()
        self.computer_board.print_board()
        while True:
            while True:
                if user_flag:
                    print("Ход Игрока")
                    user_flag = self.user.move()
                    self.user_board.print_board()
                    self.computer_board.print_board()
                    if self.computer_board.active_ships == 0:
                        winner_flag = "Игрок"
                        break
                else:
                    computer_flag = True
                    break
            if winner_flag:
                break
            while True:
                if computer_flag:
                    print("Ход Компьютера")
                    computer_flag = self.computer.move()
                    self.user_board.print_board()
                    self.computer_board.print_board()
                    if self.user_board.active_ships == 0:
                        winner_flag = "Компьютер"
                        break
                else:
                    user_flag = True
                    break
            if winner_flag:
                break
        print(f"Игра окончена! Победил {winner_flag}!")

    def start(self):
        self.greet()
        board_0 = Board()
        print("\nПодождите, пока загрузятся поля\nЭто может занять некоторое время\n")
        self.user_board = self.board_check(copy.deepcopy(board_0))
        self.computer_board = self.board_check(copy.deepcopy(board_0))
        self.computer_board.hid = True
        self.user.their_board = self.user_board
        self.user.enemy_board = self.computer_board
        self.computer.their_board = self.computer_board
        self.computer.enemy_board = self.user_board
        print("В бой!")
        self.loop()


Game().start()
