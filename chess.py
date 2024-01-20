from constants import *

# TABLE CLASS (WITH NEGATIVE INDEXING DISABLED)
class MyTable(list):
    def __getitem__(self, n):
        if n < 0:
            raise IndexError("ERROR: negative index")
        return list.__getitem__(self, n)


table = MyTable()

# ruso
# GENERATE TABLE (FINISHED)
# Table example (2x2):
# [
# [[0,0],[0,0]],
# [[0,0],[0,0]]
# ]
def generate_new_table():
    for i in range(TABLE_SIZE[0]):
        table.append([])
        for j in range(TABLE_SIZE[1]):
            table[i].append([0, 0])


# ADD DEFAULT PIECE SET
def add_pieces():
    # add pawns
    for i in range(8):
        table[1][i] = [WHITE, PAWN]
        table[6][i] = [BLACK, PAWN]
    # add figures except queen and king
    for i in range(3):
        table[0][i] = [WHITE, i + 2]
        table[0][7 - i] = [WHITE, i + 2]
        table[7][i] = [BLACK, i + 2]
        table[7][7 - i] = [BLACK, i + 2]
    # add king and queen
    table[0][3] = [WHITE, QUEEN]
    table[0][4] = [WHITE, KING]
    table[7][3] = [BLACK, QUEEN]
    table[7][4] = [BLACK, KING]


# SIGNO DE UN NÚMERO (SI ES CERO -> CERO)
# muy pero que muy útil
def sign(n):
    if n == 0:
        return 0
    else:
        return int(n / abs(n))


# POSICIÓN DEL REY, ÚNICO REY
# calcular las coordenadas del rey
def king_pos(color):
    king_i = None
    king_j = None
    for column in table:
        try:
            king_j = column.index([color, KING])
            king_i = table.index(column)
        except:
            pass
    return [king_i, king_j]


# CHECK IF THERE IS A CHECK ON BOARD
# True si lo está, False si no.
def is_check(color):
    king_i = king_pos(color)[0]
    king_j = king_pos(color)[1]
    # checar al rey en todas las direcciones
    # COLUMNAS Y DIAGONALES - reinas, torres y alfiles
    for n in range(-3, 4):  # bucle de 8 iteraciones, cada una es una dirección
        print(f"ROOK/BISHOP/QUEEN ITERATION: N = {n}")
        anulate_if_n_is_four = sign(abs(n - 4))
        for m in range(7):  # revisará como mucho 7 casillas en cada dirección
            print(f"M ITERATION: M = {m}")
            try:
                tile = table[king_i + anulate_if_n_is_four * sign(n) * (m + 1)][
                    king_j + sign(-(n ** 2) + (7 / 2) * abs(n) - (5 / 2)) * (m + 1)]
            except IndexError:
                print("nos hemos salido del tablero: ooops!")
                break
            print(tile)
            # la casilla que vamos a revisar se calcula de la siguiente manera:
            # N ES UN NÚMERO DEL -3 AL 4: en las 3 primeras iteraciones del bucle primario restaremos 1 a la coord. i
            # (ya que n será negativo), es decir, iremos verificando todas las casillas hacia abajo;
            # como la función del indice j es positiva en 2 y en -2 y cero en 1 y -1, nos facilita mucho el trabajo
            # la primera iteración será hacia abajo a secas, la segunda en diagonal hacia la derecha,
            # la tercera en diagonal hacia la izquerda, la cuarta será hacia arriba, etc.
            # el único caso con el que no obtenemos lo que queremos es con n = 4, donde queremos que revise la dcha.
            # por eso multiplicamos por una expresión que es cero cuando n = 4 y uno de lo contrario.
            if abs(n) in range(2, 4):  # si lo que estamos comprobando es una diagonal
                print("comprobando alfil")
                if tile[0] == (-color + 3) and (tile[1] == BISHOP or tile[1] == QUEEN):
                    # y lo que hay en la casilla es es un alfil o reina de color opuesto...
                    return True
                elif tile != [NO_ONE, EMPTY]:  # si hay cualquier otra cosa, salimos del bucle
                    print("Vaya! Nos hemos topado con algo que no es ni un alfil ni una reina...")
                    break
                else:
                    print("casilla vacía :)")
            else:  # si lo que estamos comprobando es fila o columna
                print("comprobando torre")
                if tile[0] == (-color + 3) and (tile[1] == ROOK or tile[1] == QUEEN):
                    return True
                elif tile != [NO_ONE, EMPTY]:
                    print("Vaya! Nos hemos topado con algo que no es ni una torre ni una reina...")
                    break
                else:
                    print("casilla vacía :)")
    # CABALLO (falta por explicar)
    for n in range(8):
        print(f"KNIGHT ITERATION: N = {n}")
        print(f"i que vamos a revisar: {int(king_i + (1 / 2) * sign(n - 3.5) - (1 / 2) + ((n // 2) - 1))}")
        print(
            f"j que vamos a revisar: {int((2 * sign((n / 2) - (n // 2)) - 1) * ((sign(-abs(n - 3.5) + 2) / 2) + (3 / 2)))}")
        try:
            tile = table[int(king_i + (1 / 2) * sign(n - 3.5) - (1 / 2) + ((n // 2) - 1))][
                int((2 * sign((n / 2) - (n // 2)) - 1) * ((sign(-abs(n - 3.5)
                                                                + 2) / 2) + (3 / 2)))]
        except IndexError:
            print("Nos hemos salido del tablero: vaya por Dios!")
            continue
        if tile == [-color + 3, KNIGHT]:
            return True
    # PEONES
    for n in range(2):
        print(f"PAWN ITERATION: N = {n}")
        try:
            tile = table[king_i - (2 * color) + 3][king_j + (2 * n - 1)]
        except IndexError:
            print("Nos hemos salido del tablero: vaya bobilibustaxxboingboing!")
            continue
        # la casilla que revisa es: índice i -> una más o menos que el índice del rey, dependiendo del color de éste
        # indice j -> una a la izqda. o dcha. dependiendo de la iteración (si es cero será una a la izqda. y viceversa)
        if tile == [-color + 3, PAWN]:
            return True
    return False


def rook_check(_table, owner, p1, p2):
    # If the rook move in a diagonal direction
    if p1[0] != p2[0] and p1[1] != p2[1]:
        return False
    # If the rook did not move
    if p1 == p2:
        return False
    # Checking table limits
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        return False
    # Checking for pieces
    delta_row = p2[0] - p1[0]
    delta_column = p2[1] - p1[1]
    # Checking if the there is a piece in p2
    if _table[p2[0]][p2[1]][0] == owner:
        return False
    # Checking for pieces in the middle
    if delta_row == 0:
        delta_s = int(delta_column / abs(delta_column))
        for i in range(p1[1] + delta_s, p2[1], delta_s):
            if _table[p2[0]][i][0] != NO_ONE:
                return False
    if delta_column == 0:
        delta_s = int(delta_row / abs(delta_row))
        for i in range(p1[0] + delta_s, p2[0], delta_s):
            if _table[i][p2[1]][0] != NO_ONE:
                return False
    return True


def pawn_check(_table, owner, p1, p2):
    delta_row = p2[0] - p1[0]
    delta_column = p2[1] - p1[1]
    if p1 == p2:
        return False
    # Checking for double move
    if owner == WHITE and p1[0] != 1 and abs(delta_row) > 1:
        return False
    if owner == BLACK and p1[0] != 6 and abs(delta_row) > 1:
        return False
    # Checking diagonal move
    if abs(delta_row) == 1 and abs(delta_column) == 1:
        if _table[p2[0]][p2[1]][0] == owner or _table[p2[0]][p2[1]][0] == EMPTY:
            return False
    # Checking column move
    if delta_column != 0:
        return False
    # Checking for backwards moves
    if owner == WHITE and delta_row < 0:
        return False
    if owner == BLACK and delta_row > 0:
        return False
    # Checking the limits
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        return False
    # Checking for an invalid forward move
    if table[p2[0]][p2[1]][0] != EMPTY:
        return False
    if abs(delta_row) > 1:
        return False
    return True


def king_check(_table, owner, p1, p2):
    # Checking for pieces
    delta_row = p2[0] - p1[0]
    delta_column = p2[1] - p1[1]
    # Checking the limits
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        return False
    # Checking for an invalid forward move
    if table[p2[0]][p2[1]][0] == owner:
        return False
    if abs(delta_row) > 1:
        return False
    if abs(delta_column) > 1:
        return False
    if p1 == p2:
        return False
    return True


def knight_check(_table, owner, p1, p2):
    # Checking table limits
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        return False
    delta_row = p2[0] - p1[0]
    delta_column = p2[1] - p1[1]
    if not ((abs(delta_row) / abs(delta_column) == 0.5) or (abs(delta_row) / abs(delta_column) == 2)):
        return False
    if abs(delta_row) > 2 or abs(delta_column) > 2:
        return False
    if table[p2[0]][p2[1]][0] == owner:
        return False
    if p1 == p2:
        return False
    return True


def bishop_check(_table, owner, p1, p2):
    # Checking table limits
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        return False
    delta_row = p2[0] - p1[0]
    delta_column = p2[1] - p1[1]
    delta_row_s = abs(delta_row) / delta_row
    delta_column_s = abs(delta_column) / delta_column
    if abs(delta_row / delta_column) != 1:
        return False
    if p1 == p2:
        return False
    if table[p2[0]][p2[1]][0] == owner:
        return False
    for i in range(1, abs(delta_row)):
        _x = (i * delta_row_s) + p1[0]
        _y = (i * delta_column_s) + p1[1]
        if _table[_x][_y][0] != EMPTY:
            return False
    return True


def queen_check(_table, owner, p1, p2):
    # Checking table limits
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        return False
    delta_row = p2[0] - p1[0]
    delta_column = p2[1] - p1[1]
    delta_row_s = abs(delta_row) / delta_row
    delta_column_s = abs(delta_column) / delta_column
    # Checking if it does not move
    if p1 == p2:
        return False
    if table[p2[0]][p2[1]][0] == owner:
        return False
    if delta_row == 0:
        delta_s = int(delta_column / abs(delta_column))
        for i in range(p1[1] + delta_s, p2[1], delta_s):
            if _table[p2[0]][i][0] != NO_ONE:
                return False
    if delta_column == 0:
        delta_s = int(delta_row / abs(delta_row))
        for i in range(p1[0] + delta_s, p2[0], delta_s):
            if _table[i][p2[1]][0] != NO_ONE:
                return False
    for i in range(1, abs(delta_row)):
        _x = (i * delta_row_s) + p1[0]
        _y = (i * delta_column_s) + p1[1]
        if _table[_x][_y][0] != EMPTY:
            return False
    return True


generate_new_table()
add_pieces()
#table[0][0] = [WHITE, KING]
#table[1][1] = [BLACK, ROOK]
#table[2][2] = [BLACK, BISHOP]
#table[1][2] = [BLACK, KNIGHT]

print(is_check(WHITE))
