import pygame

def load_image(filename,size):
    img = pygame.image.load(filename).convert()
    img = pygame.transform.scale(img, (size, size))
    return img

pygame.init()

screen_size = (500//8)*8
pygame.display.set_caption("Pengüin Chess")
screen = pygame.display.set_mode((screen_size, screen_size))

box_size = screen_size/8

# Load assets
b_background = load_image("assets/b_background.png",box_size)
b_bishop = load_image("assets/b_bishop.png",box_size)
b_king = load_image("assets/b_king.png",box_size)
b_knight = load_image("assets/b_knight.png",box_size)
b_pawn = load_image("assets/b_pawn.png",box_size)
b_queen = load_image("assets/b_queen.png",box_size)
b_rook = load_image("assets/b_rook.png",box_size)

w_background = load_image("assets/w_background.png",box_size)
w_bishop = load_image("assets/w_bishop.png",box_size)
w_king = load_image("assets/w_king.png",box_size)
w_knight = load_image("assets/w_knight.png",box_size)
w_pawn = load_image("assets/w_pawn.png",box_size)
w_queen = load_image("assets/w_queen.png",box_size)
w_rook = load_image("assets/w_rook.png",box_size)

for row in range(0,8):
    for column in range(0,8):
        if (row+column)%2 == 0:
            screen.blit(w_background,(row*box_size,column*box_size))
        else:
            screen.blit(b_background,(row*box_size,column*box_size))

pygame.display.update()
while True:pass
