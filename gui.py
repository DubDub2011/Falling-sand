import random
import pygame
import sandSimulation.sand as sand

class simulation:
    aspectRatio = (16, 9)
    screen = pygame.display.set_mode((aspectRatio[0] * 80, aspectRatio[1] * 80))
    clock = pygame.time.Clock()
    running = True

    # sand sim initialization
    sim = None
    particleLength = None
    brushDown = False
    brushSize = 5


    def __init__(self, size = 10):
        self.sim = sand.SandSimulation(self.aspectRatio[0] * size, self.aspectRatio[1] * size)
        self.particleLength = int(self.screen.get_width() / (self.aspectRatio[0] * size))

    def runSimulation(self):
        pygame.init()
        while self.running:
            self.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.brushDown = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.brushDown = False
                if event.type == pygame.MOUSEWHEEL:
                    up = event.y == 1
                    if up:
                        self.brushSize += 1
                    else:
                        self.brushSize -= 1
            
            if self.brushDown:
                self.brush(self.brushSize)

            self.sim.step()

            # the grid would hold squares to represent the sand
            # divide the size of the screen by the size of the particle
            # to get the size of square to be drawn on screen.
            for part in self.sim.particles:
                # reverse Y, as sim works in reverse order
                startPos = (part.pos[0] * self.particleLength, (self.sim.length -1 - part.pos[1]) * self.particleLength)
                rect = pygame.Rect(startPos, (self.particleLength, self.particleLength))
                color = pygame.Color(0,0,0)
                color.hsva = (part.color, 100, 100, 100)
                pygame.draw.rect(self.screen, color, rect)

            pygame.display.flip()

        pygame.quit()

    def brush(self, size):
        mousePos = pygame.mouse.get_pos()
        posX = int(mousePos[0] / self.particleLength)
        posY = int(mousePos[1] / self.particleLength)
        posY = self.sim.length - posY # reverse Y, as sim works in reverse order
        basePos = (posX, posY)
        sandPositions = [basePos]
        color = int(pygame.time.get_ticks()/ 100 % 360)

        # now create positions that are in range based on brush size
        for layer in range(size):
            dirPos = layer
            while dirPos > 0:
                sandPositions.append((basePos[0] + dirPos, basePos[1] - (layer - dirPos))) # add right to bottom
                sandPositions.append((basePos[0] - (layer - dirPos), basePos[1] - dirPos)) # add bottom to left                
                sandPositions.append((basePos[0] - dirPos, basePos[1] + (layer - dirPos))) # add left to top                
                sandPositions.append((basePos[0] + (layer - dirPos), basePos[1] + dirPos)) # add top to right                
                dirPos -= 1

        
        # remove 3/5 of the positions to make it look smoother
        random.shuffle(sandPositions)
        sandPositions = sandPositions[:int(len(sandPositions) * (3/5))]
        sortFunc = lambda pos: (pos[1], abs(basePos[0] - pos[0])) 
        sandPositions.sort(key=sortFunc)

        for pos in sandPositions:  
            inRange = True  
            inRange = inRange and 0 <= pos[0] < self.sim.width
            inRange = inRange and 0 <= pos[1] < self.sim.length
            if inRange:
                noSand = self.sim.grid[pos[0]][pos[1]] == sand.EMPTY
                if noSand:
                    self.sim.addSand(pos, color)

