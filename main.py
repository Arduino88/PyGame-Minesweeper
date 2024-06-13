import pygame
cols = 10
rows = 10

boardPixels = (800, 600)
colPixels = (boardPixels[0] // cols)
rowPixels = (boardPixels[1] // rows)




def main():
    pygame.init()
    screen = pygame.display.set_mode(boardPixels)
    pygame.display.set_caption("Minesweeper")
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((45, 45, 42))
        pygame.display.flip()

        



if __name__ == "__main__":
    main()