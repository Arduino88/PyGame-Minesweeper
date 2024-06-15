import pygame
import numpy as np
import random

cols = 10
rows = 10
mines = 15

boardPixels = (400, 400)
colPixels = (boardPixels[0] // cols)
rowPixels = (boardPixels[1] // rows)

bombGrid = [[False for _ in range(cols)] for _ in range(rows)]
flagGrid = [[False for _ in range(cols)] for _ in range(rows)]
hiddenGrid = [[None for _ in range(cols)] for _ in range(rows)]
displayGrid = [[None for _ in range(cols)] for _ in range(rows)]
margin = 5



colors = {
    'bg': (76, 76, 71),
    'unopened': (30, 30, 30),
    'mine': (150, 75, 75),
    'flag': (75, 150, 75),
    0: (150, 75, 75),
    1: (240, 90, 90),
    2: (240, 160, 90),
    3: (240, 220, 90),
    4: (240, 240, 90),
    5: (75, 150, 75),
    6: (75, 180, 75),
    7: (75, 210, 75),
    8: (75, 240, 75)
}



def main():
    def generateBombs():
        bombsX = [random.randint(0, cols - 1) for _ in range(mines)]
        bombsY = [random.randint(0, rows - 1) for _ in range(mines)]
        bombs = list(zip(bombsX, bombsY))
        print(bombs)

        for x, y in bombs:
            bombGrid[y][x] = True

        for row in bombGrid:
            print(row)
        
        pass


    def selectTile(col, row):
        displayGrid[row][col] = hiddenGrid[row][col]
        pass

    def flagTile(col, row):
        if displayGrid[row][col] is None:
            displayGrid[row][col] = 'F'
        elif displayGrid[row][col] == 'F':
            displayGrid[row][col] = None

    def loadHiddenGrid():
        directions = ((0, 1), (1, 0), (-1, 0), (0, -1), (1, -1), (-1, -1), (1, 1), (-1, 1))
        for x in range(rows):
            for y in range(cols):
                if bombGrid[y][x]:
                    continue
                counter = 0
                for dx, dy in directions:
                    tempX = x + dx
                    tempY = y + dy
                    if 0 <= tempX < cols and 0 <= tempY < rows:
                        if bombGrid[tempY][tempX]:
                            counter += 1

                hiddenGrid[y][x] = counter

        for row in hiddenGrid:
            print(row)

    pygame.init()
    generateBombs()
    loadHiddenGrid()

    mainFont = pygame.font.SysFont('segoeui', 30, bold=True)
    screen = pygame.display.set_mode(boardPixels)
    pygame.display.set_caption("Minesweeper")
    running = True
    shift = False

    while running:
        

        screen.fill(colors['bg'])
        for row in range(rows):
            for col in range(cols):
                pygame.draw.rect(screen, colors['unopened'], (colPixels * col + margin, rowPixels * row + margin, colPixels - margin, rowPixels - margin))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == 1073742049: #code for shift (this is fucked)
                shift = True
                print('shift')

            if event.type == pygame.KEYUP and event.key == 1073742049:
                shift = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                print('clicked')

                x, y = pygame.mouse.get_pos()

                x //= colPixels
                y //= rowPixels

                if shift:
                    #flag
                    print('flag tile')
                    flagTile(x, y)
                    pass

                else:
                    #open
                    print('select tile')
                    selectTile(x, y)
                    pass

                print(x, y)

        for num in (0, 1, 2, 3, 4, 5, 6, 7, 8, 'flag'):
            if type(num) == int:
                textSurface = mainFont.render(str(num), False, colors[num])
            if num == 'flag':
                textSurface = mainFont.render('F', False, colors['flag'])

            for row in range(len(displayGrid)):
                for col in range(len(displayGrid[row])):

                    if (type(num) == int and displayGrid[row][col] == num) or (num == 'flag' and displayGrid[row][col] == 'F'):
                        screen.blit(textSurface, ((colPixels * col) + colPixels // 2 - textSurface.get_width() // 2, (rowPixels * row) + colPixels // 2 - textSurface.get_height() // 2))


        pygame.display.flip()

        



if __name__ == "__main__":
    main()