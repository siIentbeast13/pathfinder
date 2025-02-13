import pygame
from threading import Thread


pygame.init()


ENUM_WALL = 0
ENUM_PATH = 1
ENUM_AGENT = 2
ENUM_TARGET = 3
ENUM_USED_PATH = 4



screen = pygame.display.set_mode((1000, 1000))

clock = pygame.time.Clock()

gameMap = []
for x in range(200):
    gameMap.append([])
    for y in range(200):
        gameMap[-1].append(ENUM_WALL)



costMap = [] 
for x in range(200):
    costMap.append([])
    for y in range(200):
        costMap[x].append(0)
def updateCost():
    if not targetPos:
        return
    updatingCost = True
    for xi, xv in enumerate(gameMap):
        for yi, yv in enumerate(xv):
            if yv == ENUM_WALL:
                costMap[xi][yi] = 99999999999999999
                continue

            xOffset = targetPos[0]-xi
            xOffset *= -1 if xOffset<0 else 1

            yOffset = targetPos[1]-yi
            yOffset *= -1 if yOffset<0 else 1

            costMap[xi][yi] = xOffset+yOffset


paintmode = ENUM_PATH

targetPos = None
agentPos = None

threadRunning = False

while True:
    screen.fill((25, 25, 25))

    for xi, xv in enumerate(gameMap):
        for yi, yv in enumerate(xv):
            if yv == ENUM_WALL:
                pygame.draw.rect(screen, (25, 25, 25), pygame.Rect(2+20*xi, 2+20*yi, 16, 16))
            if yv == ENUM_PATH:
                pygame.draw.rect(screen, (200, 200, 200), pygame.Rect(2+20*xi, 2+20*yi, 16, 16))
            if yv == ENUM_AGENT:
                pygame.draw.rect(screen, (0, 0, 200), pygame.Rect(2+20*xi, 2+20*yi, 16, 16))
            if yv == ENUM_TARGET:
                pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(2+20*xi, 2+20*yi, 16, 16))
            if yv == ENUM_USED_PATH:
                pygame.draw.rect(screen, (0, 200, 200), pygame.Rect(2+20*xi, 2+20*yi, 16, 16))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key >= pygame.K_1 and event.key <= pygame.K_4:
                paintmode = event.key - pygame.K_1
                print(f"Paintmode set to", event.key - pygame.K_0)
            elif event.key == pygame.K_r:
                for xi, xv in enumerate(gameMap):
                    for yi, yv in enumerate(xv):
                        if yv == ENUM_USED_PATH:
                            gameMap[xi][yi] = ENUM_PATH


        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            tilePos = (int(mousePos[0]/20), int(mousePos[1]/20))

            gameMap[tilePos[0]][tilePos[1]] = paintmode

            if paintmode == ENUM_AGENT:
                if agentPos : gameMap[agentPos[0]][agentPos[1]] = ENUM_WALL
                agentPos = tilePos
            if paintmode == ENUM_TARGET:
                if targetPos : gameMap[targetPos[0]][targetPos[1]] = ENUM_WALL
                targetPos = tilePos

            updateCost()

        
    
    pygame.display.update()
    clock.tick(60)