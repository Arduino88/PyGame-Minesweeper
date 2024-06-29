import pygame
from collections import deque
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
    'bg': (192, 192, 192),
    'unopened': (200, 200, 200),
    'opened' :(220, 220, 220),
    'mine': (150, 75, 75),
    'flag': (255, 0, 0),
    0: (150, 75, 75),
    1: (0, 0, 221),
    2: (39, 126, 39),
    3: (241, 0, 1),
    4: (3, 3, 132),
    5: (112, 16, 0),
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



    def selectTile(col, row):
        nonlocal running
        if bombGrid[row][col] and displayGrid[row][col] != 'F':
            running = False


        if displayGrid[row][col] is None:
            displayGrid[row][col] = hiddenGrid[row][col]
            if displayGrid[row][col] == 0:
                print('BFS')
                #bfs
                seen = set()
                q = deque()
                q.append((col, row))
                while q:
                    tempCol, tempRow = q.popleft()
                    if (tempCol, tempRow) not in seen:
                        seen.add((tempCol, tempRow))

                    else: 
                        continue
                    
                    displayGrid[tempRow][tempCol] = hiddenGrid[tempRow][tempCol]
                    if displayGrid[tempRow][tempCol] != 0:
                        continue

                    for dx, dy in ((0, -1), (-1, 0), (0, 1), (1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
                        newCol = tempCol + dx
                        newRow = tempRow + dy
                        if 0 <= newCol < cols and 0 <= newRow < rows:
                            q.append((newCol, newRow))


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
    flag = pygame.image.load('assets/flag.png')
    flag = pygame.transform.scale(flag, (25, 25))
    mainFont = pygame.font.SysFont('segoeui', 30, bold=True)
    screen = pygame.display.set_mode(boardPixels)
    pygame.display.set_caption("Minesweeper")
    running = True
    shift = False

    while running:
        

        screen.fill(colors['bg'])
        for row in range(rows):
            for col in range(cols):
                if displayGrid[row][col] is None:
                    pygame.draw.rect(screen, colors['unopened'], (colPixels * col + margin, rowPixels * row + margin, colPixels - margin, rowPixels - margin))
                else:
                    pygame.draw.rect(screen, colors['opened'], (colPixels * col + margin, rowPixels * row + margin, colPixels - margin, rowPixels - margin))

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

        for num in (1, 2, 3, 4, 5, 6, 7, 8, 'flag'):
            if type(num) == int:
                textSurface = mainFont.render(str(num), False, colors[num])
            if num == 'flag':
                textSurface = flag

            for row in range(len(displayGrid)):
                for col in range(len(displayGrid[row])):

                    if (type(num) == int and displayGrid[row][col] == num) or (num == 'flag' and displayGrid[row][col] == 'F'):
                        screen.blit(textSurface, ((colPixels * col) + colPixels // 2 - textSurface.get_width() // 2, (rowPixels * row) + colPixels // 2 - textSurface.get_height() // 2))


        pygame.display.flip()

        



if __name__ == "__main__":
    main()