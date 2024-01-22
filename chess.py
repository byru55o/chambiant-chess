from constants import *
from copy import deepcopy

king_moved = [False, False]  # 1er elemento -> ¿Han movido el rey las blancas? 2o elemento -> ¿" " " " las negras?
rook_moved = [False, False, False, False]  # Lo mismo para cada torre -> índices: [0,0] ; [0,7] ; [7,0] ; [7,7]


# TABLE CLASS (WITH NEGATIVE INDEXING DISABLED)
class MyTable(list):
    def __getitem__(self, n):
        if n < 0:
            raise IndexError("ERROR: negative index")
        return list.__getitem__(self, n)


table = MyTable()

# ruso
# TO DO: remove testing lines


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
def king_pos(_table, color):
    king_i = None
    king_j = None
    for column in _table:
        try:
            king_j = column.index([color, KING])
            king_i = _table.index(column)
        except:
            pass
    return [king_i, king_j]


# CHECK IF THERE IS A CHECK ON BOARD
# True si lo está, False si no.
def is_check(_table, color):
    king_i = king_pos(_table, color)[0]
    king_j = king_pos(_table, color)[1]
    # checar al rey en todas las direcciones
    # COLUMNAS Y DIAGONALES - reinas, torres y alfiles
    for n in range(-3, 4):  # bucle de 8 iteraciones, cada una es una dirección
        for m in range(7):  # revisará como mucho 7 casillas en cada dirección
            try:
                if n != 3:
                    tile = _table[king_i + sign(n) * (m + 1)][
                        king_j + sign(-(n ** 2) + (7 / 2) * abs(n) - (5 / 2)) * (m + 1)]
                else:  # Caso excepción -> columna hacia la derecha
                    tile = _table[king_i][king_j + (m + 1)]
            except IndexError:
                break
            print(tile)
            # la casilla que vamos a revisar se calcula de la siguiente manera:
            # N ES UN NÚMERO DEL -3 AL 4: en las 3 primeras iteraciones del bucle primario restaremos 1 a la coord. i
            # (ya que n será negativo), es decir, iremos verificando todas las casillas hacia abajo;
            # como la función del indice j es positiva en 2 y en -2 y cero en 1 y -1, nos facilita mucho el trabajo
            # la primera iteración será hacia abajo a secas, la segunda en diagonal hacia la derecha,
            # la tercera en diagonal hacia la izquerda, la cuarta será hacia arriba, etc.
            # el único caso con el que no obtenemos lo que queremos es con n = 3, donde queremos que revise la dcha.
            # por eso multiplicamos por una expresión que es cero cuando n = 3 y uno de lo contrario.
            if abs(n) in range(2, 4):  # si lo que estamos comprobando es una diagonal
                if tile[0] == (-color + 3) and (tile[1] == BISHOP or tile[1] == QUEEN):
                    # y lo que hay en la casilla es es un alfil o reina de color opuesto...
                    return True
                elif tile != [NO_ONE, EMPTY]:  # si hay cualquier otra cosa, salimos del bucle
                    break
            else:  # si lo que estamos comprobando es fila o columna
                if tile[0] == (-color + 3) and (tile[1] == ROOK or tile[1] == QUEEN):
                    return True
                elif tile != [NO_ONE, EMPTY]:
                    break
    # CABALLO (falta por explicar)
    for n in range(8):
        try:
            tile = _table[int(king_i + (1 / 2) * sign(n - 3.5) - (1 / 2) + ((n // 2) - 1))][
                int(king_j + (2 * sign((n / 2) - (n // 2)) - 1) * ((sign(-abs(n - 3.5) + 2) / 2) + (3 / 2)))]
        except IndexError:
            continue
        if tile == [-color + 3, KNIGHT]:
            return True
    # PEONES
    for n in range(2):
        try:
            tile = _table[king_i - (2 * color) + 3][king_j + (2 * n - 1)]
        except IndexError:
            continue
        # la casilla que revisa es: índice i -> una más o menos que el índice del rey, dependiendo del color de éste
        # indice j -> una a la izqda. o dcha. dependiendo de la iteración (si es cero será una a la izqda. y viceversa)
        if tile == [-color + 3, PAWN]:
            return True
    return False


def rook_legal(p1, p2):
    owner = table[p1[0]][p1[1]][0]

    # Basic checks (for all functions)
    if p1 == p2:
        print("rook_check: position unchanged")
        return False
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        print("rook_check: position excceded table limits")
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        print("rook_check: position excceded table limits")
        return False
    if table[p2[0]][p2[1]][0] == owner:
        print("rook_check: owner trying to eat owner")
        return False

    # Checking direction
    if p1[0] != p2[0] and p1[1] != p2[1]:
        print("rook_check: rook can not move in both axis at a time")
        return False

    # Calculating deltas
    delta_column = p2[0] - p1[0]
    delta_column_s = sign(delta_column)
    delta_row = p2[1] - p1[1]
    delta_row_s = sign(delta_row)

    # Checking for pieces in the way
    for i in range(1, max([abs(delta_column), abs(delta_row)])):
        c = int((i * delta_column_s) + p1[0])
        r = int((i * delta_row_s) + p1[1])
        if table[c][r][0] != EMPTY:
            print("rook_check: there are pieces in the way")
            return False
    return True


def pawn_legal(p1, p2):
    owner = table[p1[0]][p1[1]][0]

    # Basic checks (for all functions)
    if p1 == p2:
        print("pawn_check: position unchanged")
        return False
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        print("pawn_check: position excceded table limits")
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        print("pawn_check: position excceded table limits")
        return False
    if table[p2[0]][p2[1]][0] == owner:
        print("pawn_check: owner trying to eat owner")
        return False

    # Calculating deltas
    delta_column = p2[0] - p1[0]
    delta_column_s = sign(delta_column)
    delta_row = p2[1] - p1[1]
    delta_row_s = sign(delta_row)

    # Checking it does not move backwards
    if owner == BLACK and delta_column > 0:
        print("pawn_check: can not move backwards")
        return False
    if owner == WHITE and delta_column < 0:
        print("pawn_check: can not move backwards")
        return False

    # Checking for double move
    if owner == BLACK and p1[0] == 6:
        if table[p2[0]][p2[1]][0] != NO_ONE:
            print("pawn_check: can not capture on double move")
            return False
        if abs(delta_column) > 2:
            print("pawn_check: can not move more than 2 block")
            return False
    elif owner == WHITE and p1[0] == 1:
        if table[p2[0]][p2[1]][0] != NO_ONE:
            print("pawn_check: can not capture on double move")
            return False
        if abs(delta_column) > 2:
            print("panw_check: can not move more than 2 blocks")
            return False

    # Checking for forward and diagonal capture 
    else:
        if abs(delta_column) > 1:
            return False

        # Simple forward move
        if abs(delta_row) == 0:
            if table[p2[0]][p2[1]][0] != NO_ONE:
                print("pawn_check: can not capture on forward move")
                return False

        # Diagonal capture
        else:
            if abs(delta_column/delta_row) != 1:
                print("pawn_check: not moving in both axis equally")
                return False
            if table[p2[0]][p2[1]][0] == owner or table[p2[0]][p2[1]][0] == NO_ONE:
                print("pawn_check: pawn needs to capture for diagonal move")
                return False

    return True


def king_legal(p1, p2):
    owner = table[p1[0]][p1[1]][0]

    # Basic checks (for all functions)
    if p1 == p2:
        print("king_check: position unchanged")
        return False
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        print("king_check: position excceded table limits")
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        print("king_check: position excceded table limits")
        return False
    if table[p2[0]][p2[1]][0] == owner:
        print("king_check: owner trying to eat owner")
        return False

    # Calculating deltas
    delta_column = p2[0] - p1[0]
    delta_column_s = sign(delta_column)
    delta_row = p2[1] - p1[1]
    delta_row_s = sign(delta_row)

    # Checking that it only moves one box
    if abs(delta_column) > 1:
        print("king_check: moving more than one box")
        return False
    if abs(delta_row) > 1:
        print("king_check: moving more than one box")
        return False
    return True


def knight_legal(p1, p2):
    owner = table[p1[0]][p1[1]][0]

    # Basic checks (for all functions)
    if p1 == p2:
        print("knight_check: position unchanged")
        return False
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        print("knight_check: position excceded table limits")
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        print("knight_check: position excceded table limits")
        return False
    if table[p2[0]][p2[1]][0] == owner:
        print("knight_check: owner trying to eat owner")
        return False

    # Calculating deltas
    delta_column = p2[0] - p1[0]
    delta_column_s = sign(delta_column)
    delta_row = p2[1] - p1[1]
    delta_row_s = sign(delta_row)

    # Checking if it is only moving in one axis
    if delta_column == 0 or delta_row == 0:
        print("knight_check: only moving in one axis")
        return False

    # Checking that is moves in L
    if not ((abs(delta_row) / abs(delta_column) == 0.5) or (abs(delta_row) / abs(delta_column) == 2)):
        print("knight_check: not moving in L")
        return False

    # Checking it is not moving more than 2 box in axis
    if abs(delta_row) > 2 or abs(delta_column) > 2:
        print("knight_check: moving more than two boxes")
        return False
    return True


def bishop_legal(p1, p2):
    owner = table[p1[0]][p1[1]][0]

    # Basic checks (for all functions)
    if p1 == p2:
        print("bishop_check: position unchanged")
        return False
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        print("bishop_check: position excceded table limits")
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        print("bishop_check: position excceded table limits")
        return False
    if table[p2[0]][p2[1]][0] == owner:
        print("bishop_check: owner trying to eat owner")
        return False

    # Calculating deltas
    delta_column = p2[0] - p1[0]
    delta_column_s = sign(delta_column)
    delta_row = p2[1] - p1[1]
    delta_row_s = sign(delta_row)

    # Checking if it is only moving in one axis
    if delta_row == 0 or delta_column == 0:
        print("bishop_check: only moving in one axis")
        return False

    # Checking that moves equally on both axis
    if abs(delta_row / delta_column) != 1:
        print("bishop_check: not moving in both axis equally")
        return False

    # Checking for pieces in the middle
    for i in range(1, max([abs(delta_column), abs(delta_row)])):
        c = int((i * delta_column_s) + p1[0])
        r = int((i * delta_row_s) + p1[1])
        if table[c][r][0] != EMPTY:
            print("bishop_check: there are pieces in the way")
            return False
    return True


def queen_legal(p1, p2):
    owner = table[p1[0]][p1[1]][0]

    # Basic checks (for all functions)
    if p1 == p2:
        print("queen_check: position unchanged")
        return False
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        print("queen_check: position excceded table limits")
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        print("queen_check: position excceded table limits")
        return False
    if table[p2[0]][p2[1]][0] == owner:
        print("queen_check: owner trying to eat owner")
        return False

    # Calculating deltas
    delta_column = p2[0] - p1[0]
    delta_column_s = sign(delta_column)
    delta_row = p2[1] - p1[1]
    delta_row_s = sign(delta_row)

    # Checking if it is moving on both axis
    if delta_column != 0 and delta_row != 0:
        if abs(delta_column / delta_row) != 1:
            print("queen_check: not moving equally on both axis")
            return False

    # Checking for pieces in the middle
    for i in range(1, max([abs(delta_column), abs(delta_row)])):
        c = int((i * delta_column_s) + p1[0])
        r = int((i * delta_row_s) + p1[1])
        if table[c][r][0] != EMPTY:
            print("queen_check: there are pieces in the way")
            return False

    return True


def castle(p1, p2):
    print("checking castle")
    owner = table[p1[0]][p1[1]][0]

    # Basic checks (for all functions)
    if p1 == p2:
        print("king_check: position unchanged")
        return False
    if p2[0] > (TABLE_SIZE[0] - 1) or p2[0] < 0:
        print("king_check: position excceded table limits")
        return False
    if p2[1] > (TABLE_SIZE[1] - 1) or p2[1] < 0:
        print("king_check: position excceded table limits")
        return False

    # Calculating deltas
    print("calculating deltas...")
    delta_column = p2[0] - p1[0]
    delta_column_s = sign(delta_column)
    delta_row = p2[1] - p1[1]
    delta_row_s = sign(delta_row)
    # Checking for not horizontal moves
    if delta_column != 0:
        print("castle: owner not moving horizontally")
        return False
    # Checking that the king hasn't moved
    if king_moved[owner-1]:
        print("castle: king has moved")
        return False
    # Checking that the king is not in check
    if is_check(table, owner):
        print("castle: king is in check")
        return False
    # Checking for pieces in the way
    print("castle: checking pieces in the way")
    for i in range(1, abs(delta_row)):
        c = int((i * delta_row_s) + p1[1])
        if table[(owner-1)*7][c][0] != EMPTY:
            print("castle: there are pieces in the way")
            return False
    # Checks for LONG CASTLE
    if p2[1] == 0:
        print("castle: attempting a long castle")
        # Check whether the rook moved
        if rook_moved[(owner-1)*2+1]:
            print("castle: the rook moved")
            return False
        # Check is_check in the two tiles at left of p1
        table_1 = deepcopy(table)
        table_1[p1[0]][p1[1]][0] = NO_ONE
        table_1[p1[0]][p1[1]][1] = EMPTY
        table_1[p1[0]][p1[1]-1][0] = owner
        table_1[p1[0]][p1[1]-1][1] = KING

        table_2 = deepcopy(table)
        table_2[p1[0]][p1[1]][0] = NO_ONE
        table_2[p1[0]][p1[1]][1] = EMPTY
        table_2[p1[0]][p1[1]-2][0] = owner
        table_2[p1[0]][p1[1]-2][1] = KING
        if is_check(table_1, owner) or is_check(table_2, owner):
            print("castle: the king passes through check")
            return False
        else:
            print("castle: LONG CASTLE IS GUD")
            return -1

    # Checks for SHORT CASTLE
    elif p2[1] == 7:
        print("castle: attempting short castle")
        # Check whether the rook moved
        if rook_moved[(owner-1)*2+1]:
            print("castle: the rook moved before")
            return False
        # Check is_check in the two tiles at right of p1
        table_1 = deepcopy(table)
        table_1[p1[0]][p1[1]][0] = NO_ONE
        table_1[p1[0]][p1[1]][1] = EMPTY
        table_1[p1[0]][p1[1]+1][0] = owner
        table_1[p1[0]][p1[1]+1][1] = KING
        print(table_1)

        table_2 = deepcopy(table)
        table_2[p1[0]][p1[1]][0] = NO_ONE
        table_2[p1[0]][p1[1]][1] = EMPTY
        table_2[p1[0]][p1[1]+2][0] = owner
        table_2[p1[0]][p1[1]+2][1] = KING
        if is_check(table_1, owner) or is_check(table_2, owner):
            print("castle: king passes through check")
            return False
        else:
            print("castle: SHORT CASTLE IS GUD")
            return 1
    else:  # No rook selected
        print("castle: no rook selected")


# Global function to check ANY move
# Undone/broken pieces: pawn
def legal_move(p1, p2):
    piece = table[p1[0]][p1[1]][1]
    piece_color = table[p1[0]][p1[1]][0]
    new_table = MyTable(deepcopy(table))
    new_table[p1[0]][p1[1]][0] = NO_ONE
    new_table[p1[0]][p1[1]][1] = EMPTY
    new_table[p2[0]][p2[1]][0] = piece_color
    new_table[p2[0]][p2[1]][1] = piece
    if table == new_table:
        print("tables are the same... BOF")
    else:
        print("tables are not the same")
        print(table)
        print(new_table)
    if piece == KNIGHT:
        print(f"knight check: {knight_legal(p1, p2)}\nis_check: {is_check(new_table, piece_color)}")
        return knight_legal(p1, p2) and not is_check(new_table, piece_color)
    elif piece == QUEEN:
        print(f"queen check: {queen_legal(p1, p2)}\nis_check: {is_check(new_table, piece_color)}")
        return queen_legal(p1, p2) and not is_check(new_table, piece_color)
    elif piece == PAWN:
        print(f"pawn check: {pawn_legal(p1, p2)}\nis_check: {is_check(new_table, piece_color)}")
        return pawn_legal(p1, p2) and not is_check(new_table, piece_color)
    elif piece == BISHOP:
        print(f"bishop check: {bishop_legal(p1, p2)}\nis_check: {is_check(new_table, piece_color)}")
        return bishop_legal(p1, p2) and not is_check(new_table, piece_color)
    elif piece == KING:
        make_normal_move = king_legal(p1, p2) and not is_check(new_table, piece_color)
        print(f"king check: {king_legal(p1, p2)}\nis_check: {is_check(new_table, piece_color)}")
        if make_normal_move:
            king_moved[piece_color-1] = True  # Para comprobar la legalidad del enroque
        return make_normal_move

    elif piece == ROOK:
        make_move = rook_legal(p1, p2) and not is_check(new_table, piece_color)
        print(f"rook check: {rook_legal(p1, p2)}\nis_check: {is_check(new_table, piece_color)}")
        if make_move and ((p1[0] == 0 or p1[0] == 7) and (p1[1] == 0 or p1[1] == 7)):  # [0,0] ; [0,7] ; [7,7]; [7,0]
            rook_moved[int((2/7)*p1[0]+(1/7)*p1[1])] = True  # Para comprobar la legalidad del enroque
            # 0x+0y = 0 ; 0x+7y = 1 ; 7x+0y = 2 ; 7x+7y = 3 => x = 2/7 ; y = 1/7
        return make_move
    return True


generate_new_table()
add_pieces()
