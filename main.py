# DECLARATION OF CONSTANTS
TABLE_SIZE = [8, 8]
table = []

EMPTY = 0
PAWN = 1
ROOK = 2
KNIGHT = 3
BISHOP = 4
KING = 5
QUEEN = 6

NO_ONE = 0
WHITE = 1
BLACK = 2


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

    # ADD ROOK ON (5, 4) -> e6
    table[5][4] = [BLACK, ROOK]


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
    #checar al rey en todas las direcciones
    #columna
    for i in range():
        print(m)
        # la potencia no altera la cuenta, a menos que delta sea cero
        # si delta es cero (el Rey está en la misma columna que nuestra pieza) -> el bucle no se efectuará
        # si delta es positivo (el Rey está a la derecha) -> se repite j veces (coincide con el número de casillas
        # que quedan a la izqda.
        # si delta es negativo (el Rey está a la izquierda) -> se repite 7 - j veces (el número de casillas que
        # quedan a la derecha).
        tile = table[i - sign(delta2) * (m + 1)][j - sign(delta(m + 1))]
        if tile != [NO_ONE, EMPTY]:
            return False  # hay otra pieza antes de toparnos con la reina o con la torre/alfil.
        elif abs(delta) != abs(delta):  # si es en horizontal o vertical
            if tile == [-color + 1, ROOK] or [-color + 1, QUEEN]:
                return True  # hay una torre o reina y la pieza está justo entre el Rey y aquella.
        else:
            if tile == [-color + 1, BISHOP] or [-color + 1, QUEEN]:
                return True  # hay un alfil o reina y la pieza está justo entre el Rey y aquella.
    else:
        return False  # el Rey no está en ninguna dirección que coincida con la pieza


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
    return True

def knight_check(_table, owner, p1, p2):
    # Checking table limits
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        return False
    delta_row = p2[0] - p1[0]
    delta_column = p2[1] - p1[1]
    if not ((abs(delta_row)/abs(delta_column) == 0.5) or (abs(delta_row)/abs(delta_column) == 2)):
        return False
    if abs(delta_row) > 2 or abs(delta_column) > 2:
        return False
    if table[p2[0]][p2[1]][0] == owner:
        return False
    return True
