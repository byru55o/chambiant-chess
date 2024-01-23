from chess import *
import pygame


def load_image(filename, size):
    img = pygame.image.load(filename).convert_alpha()
    img = pygame.transform.smoothscale(img, (size, size))
    return img


def play_sound(audio):
    channel = pygame.mixer.Sound.play(audio)
    while channel.get_busy():
        pygame.time.wait(20)


pygame.mixer.init()
pygame.init()

clock = pygame.time.Clock()

screen_size = (RESOLUTION // 8) * 8
pygame.display.set_caption("Pengüin Chess")
screen = pygame.display.set_mode((screen_size, screen_size))

box_size = screen_size / 8

# Load assets
s_background = load_image("assets/s_background.png", box_size)
s_check = load_image("assets/s_check.png",box_size)

b_background = load_image("assets/b_background.png", box_size)
b_bishop = load_image("assets/b_bishop.png", box_size)
b_king = load_image("assets/b_king.png", box_size)
b_knight = load_image("assets/b_knight.png", box_size)
b_pawn = load_image("assets/b_pawn.png", box_size)
b_queen = load_image("assets/b_queen.png", box_size)
b_rook = load_image("assets/b_rook.png", box_size)

w_background = load_image("assets/w_background.png", box_size)
w_bishop = load_image("assets/w_bishop.png", box_size)
w_king = load_image("assets/w_king.png", box_size)
w_knight = load_image("assets/w_knight.png", box_size)
w_pawn = load_image("assets/w_pawn.png", box_size)
w_queen = load_image("assets/w_queen.png", box_size)
w_rook = load_image("assets/w_rook.png", box_size)

p_move = pygame.mixer.Sound("assets/p_move.wav")
p_capture = pygame.mixer.Sound("assets/p_capture.wav")
p_notify = pygame.mixer.Sound("assets/p_notify.wav")
p_oh_my_god = pygame.mixer.Sound("assets/oh_my_god.wav")

# Matrix ordered by constant values
b_matrix = [None, b_pawn, b_rook, b_knight, b_bishop, b_king, b_queen]
w_matrix = [None, w_pawn, w_rook, w_knight, w_bishop, w_king, w_queen]

# Turn change matrix
c_matrix = [None, BLACK, WHITE]

# Main game loop
turn = WHITE
change = False
selected = False
from_box = (0, 0)
to_box = (0, 0)

king_position = (0,0)
check = False
while True:

    # Draw base table
    for row in range(0, 8):
        for column in range(0, 8):
            if (row + column) % 2 == 0:
                screen.blit(w_background, (row * box_size, column * box_size))
            else:
                screen.blit(b_background, (row * box_size, column * box_size))

    # Drawing selected box (if selected)
    if selected:
        screen.blit(s_background, (from_box[1] * box_size, (7 - from_box[0]) * box_size))

    if check:
        screen.blit(s_check, (king_position[1] * box_size, (7 - king_position[0]) * box_size))

    # Drawing pieces on the table
    for row in range(0, 8):
        for column in range(0, 8):
            owner = table[column][row][0]
            piece = table[column][row][1]
            if owner != NO_ONE:
                if owner == WHITE:
                    screen.blit(w_matrix[piece], (row * box_size, (7 - column) * box_size))
                if owner == BLACK:
                    screen.blit(b_matrix[piece], (row * box_size, (7 - column) * box_size))

    # Handling clicks
    ev = pygame.event.get()
    for event in ev:
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_position = pygame.mouse.get_pos()
            row = int(mouse_position[0] // box_size)
            column = int(7 - (mouse_position[1] // box_size))
            print(f"Clicked piece [{column},{row}]")
            if selected:
                to_box = (column, row)
                if (table[from_box[0]][from_box[1]][1] == KING and table[column][row][1] == ROOK and
                        (table[from_box[0]][from_box[1]][0] == table[column][row][0])):
                    print("ATTEMPTING CASTLE!!!!!")
                    castle_squares = castle(from_box, to_box)
                    print(f"CASTLE SQUARES: {castle_squares}")
                    if castle_squares != 0:
                        selected = False

                        # Playing_sound
                        play_sound(p_move)

                        # Placing king
                        table[from_box[0]][from_box[1]+2*castle_squares][0] = table[from_box[0]][from_box[1]][0]
                        table[from_box[0]][from_box[1]+2*castle_squares][1] = table[from_box[0]][from_box[1]][1]
                        table[from_box[0]][from_box[1]][0] = NO_ONE
                        table[from_box[0]][from_box[1]][1] = EMPTY

                        # Placing rook
                        table[from_box[0]][from_box[1]+castle_squares][0] = table[column][row][0]
                        table[from_box[0]][from_box[1]+castle_squares][1] = table[to_box[0]][to_box[1]][1]
                        table[to_box[0]][to_box[1]][0] = NO_ONE
                        table[to_box[0]][to_box[1]][1] = EMPTY

                        print(table)
                        change = True

                elif table[column][row][0] != turn:
                    move_type = legal_move(from_box, to_box)
                    selected = False
                    if move_type == "en passant":
                        # Playing sound
                        play_sound(p_oh_my_god)

                        # Placing the pawn
                        table[to_box[0]][to_box[1]][0] = table[from_box[0]][from_box[1]][0]
                        table[to_box[0]][to_box[1]][1] = table[from_box[0]][from_box[1]][1]
                        # Removing pawn from table
                        table[from_box[0]][from_box[1]][0] = NO_ONE
                        table[from_box[0]][from_box[1]][1] = EMPTY

                        # Removing the pawn
                        table[to_box[0]+(2*turn-3)][to_box[1]][0] = NO_ONE
                        table[to_box[0]+(2*turn-3)][to_box[1]][1] = EMPTY
                    elif move_type:
                        # Playing sound
                        if table[column][row][0] == c_matrix[turn]:
                            play_sound(p_capture)
                        else:
                            play_sound(p_move)

                        # Copying piece to table
                        table[to_box[0]][to_box[1]][0] = table[from_box[0]][from_box[1]][0]
                        table[to_box[0]][to_box[1]][1] = table[from_box[0]][from_box[1]][1]

                        # Removing piece from table
                        table[from_box[0]][from_box[1]][0] = NO_ONE
                        table[from_box[0]][from_box[1]][1] = EMPTY

                        # Getting if the king is in danger
                        check = is_check(table, c_matrix[turn])
                        if check:
                            king_position = king_pos(table, c_matrix[turn])

                        # Change turn
                        change = True
                else:
                    selected = False
            else:
                if table[column][row][0] == turn:
                    selected = True
                    from_box = (column, row)

    # Switching turns
    if change:
        change = False
        turn = c_matrix[turn]

    pygame.display.update()
    clock.tick(FPS)
