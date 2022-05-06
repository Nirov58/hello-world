
field = [[" ", "1", "2", "3", "\n"],
         ["1", "-", "-", "-", "\n"],
         ["2", "-", "-", "-", "\n"],
         ["3", "-", "-", "-", "\n"]]
free_cells = 9


def unpack(b):
    print("".join(list(map(" ".join, b))))


def win_conds_check(c):
    for i in range(1, 4):
        if any([
                c[1][1] == c[2][2] == c[3][3] != "-",
                c[1][3] == c[2][2] == c[3][1] != "-",
                c[i][1] == c[i][2] == c[i][3] != "-",
                c[1][i] == c[2][i] == c[3][i] != "-"]):
            return True
    return False


def place_mark(m):
    x = int(input("Введите координату x: "))
    y = int(input("Введите координату y: "))
    if not field[y][x] == "-":
        print("Ячейка уже занята!\nВыберете другую ячейку")
        place_mark(m)
    field[y][x] = field[y][x].replace("-", m)
    unpack(field)


def first_player():
    print("Ход Игрока 1.")
    place_mark("x")


def second_player():
    print("Ход Игрока 2.")
    place_mark("o")


print("Добро пожаловать в игру 'Крестики-нолики'!\n"
      "Чтобы поставить крестик или нолик, введите в командную строку координаты выбранной ячейки\n"
      "Сначала введите координату по горизонтали (x), а затем по вертикали (y)\n"
      "Первый игрок ставит крестики, второй - нолики\n")

unpack(field)

while True:
    first_player()
    free_cells -= 1
    if free_cells <= 0:
        status = "Ничья!"
        break
    if win_conds_check(field):
        status = "Победил Игрок 1!"
        break
    second_player()
    free_cells -= 1
    if win_conds_check(field):
        status = "Победил Игрок 2!"
        break
print("Игра окончена!", status, sep="\n")
