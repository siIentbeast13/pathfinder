import pygame
import time
from threading import Thread


pygame.init()


ENUM_WALL = 0
ENUM_PATH = 1
ENUM_AGENT = 2
ENUM_TARGET = 3
ENUM_USED_PATH = 4



screen = pygame.display.set_mode((1000, 1000))


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






class Node:
    def __init__(self, pos, step=0, parent=None):
        self.pos = pos
        self.step = step
        self.cost = step + costMap[pos[0]][pos[1]]
        self.parent = parent
    
    def process(self):
        explored.append(self.pos)

        neighbours = [] 
        toExplore = ((0,-1), (0, 1), (1, 0), (-1, 0))
        for x, y in toExplore:
                if (x,y) == (0,0): continue
                exploringPos = (self.pos[0]+x, self.pos[1]+y)
                if exploringPos[0] < 0 or exploringPos[0] >= 200 or exploringPos[1] < 0 or exploringPos[1] >= 200 : continue

                isWall = not gameMap[exploringPos[0]][exploringPos[1]]
                inFrontier = False
                for node in frontier:
                    if inFrontier : break
                    inFrontier = node.pos == exploringPos
                if exploringPos in explored or isWall: continue

                neighbours.append(exploringPos)

        for neighbour in neighbours:
            frontier.append(Node(neighbour, self.step+1, self))
    
    def __repr__(self):
        return "Node:"+str(self.pos)+"Cost:"+str(self.cost)







threadRunning = False
def startPathfinding():
    global frontier, explored, found
    threadRunning = True

    frontier = [Node(agentPos)]
    explored = []

    targetNode = None
    while True:
        if len(frontier) == 0:
            print("No path found")
            return

        selectedNode = frontier[0]
        indexOfSelected = 0
        for i, node in enumerate(frontier):
            if node.cost < selectedNode.cost:
                selectedNode = node
                indexOfSelected = i
        frontier.pop(indexOfSelected)
        
        if selectedNode.pos == targetPos:
            targetNode = selectedNode
            break
        selectedNode.process()
    
    currentNode = targetNode.parent
    while currentNode.pos != agentPos:
        gameMap[currentNode.pos[0]][currentNode.pos[1]] = ENUM_USED_PATH
        currentNode = currentNode.parent


    threadRunning = False







mouseDown = False
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
            elif event.key == pygame.K_RETURN:
                if threadRunning:
                    print("Pathfinding already running")
                    continue
                
                if not (agentPos and targetPos):
                    print("No agent or target found")
                    continue
                    
                thread = Thread(target=startPathfinding)
                thread.start()
            elif event.key == pygame.K_r:
                for xi, xv in enumerate(gameMap):
                    for yi, yv in enumerate(x):
                        if yv == ENUM_USED_PATH:
                            gameMap[xi][yi] = ENUM_PATH

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False



    if mouseDown:
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