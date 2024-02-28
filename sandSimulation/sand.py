import copy
import random
import time

class Particle:
    grid = [[]]
    pos = (0, 0)
    color = 0
    grav = 1
    gravBase = 2
    static = False


    def __init__(self, grid, position, color):
        self.grid = grid
        self.pos = position
        self.grid[self.pos[0]][self.pos[1]] = OCCUPIED
        self.color = color

    def fall(self):
        if self.static:
            return
        
        grid = self.grid
        for _ in range(int(self.grav)):
            x = self.pos[0]
            y = self.pos[1]

            # can't fall any futher
            if y == 0 or grid[x][y] == STATIC:
                grid[x][y] = STATIC
                self.static = True
                return

            # check below, fall into space if empty
            spaceBelow = grid[x][y-1] == EMPTY
            if spaceBelow:
                grid[x][y] = EMPTY
                self.pos = (x, y-1)
                grid[x][y-1] = OCCUPIED
                continue

            # sand should trickle down the side if there is space
            spaceBelowLeft = x != 0 and grid[x-1][y-1] == EMPTY 
            spaceBelowRight = x != len(grid)-1 and grid[x+1][y-1] == EMPTY
            if spaceBelowLeft and spaceBelowRight:
                fallLeft = bool(random.choice([True, False]))
                if fallLeft:
                    self.pos = (x-1, y-1)
                    grid[x][y] = EMPTY
                    grid[x-1][y-1] = OCCUPIED
                    self.grav -= self.gravBase
                else:
                    self.pos = (x+1, y-1)
                    grid[x][y] = EMPTY
                    grid[x+1][y-1] = OCCUPIED
                    self.grav -= self.gravBase
            elif spaceBelowLeft:
                self.pos = (x-1, y-1)
                grid[x][y] = EMPTY
                grid[x-1][y-1] = OCCUPIED
                self.grav -= self.gravBase
            elif spaceBelowRight:
                self.pos = (x+1, y-1)
                grid[x][y] = EMPTY
                grid[x+1][y-1] = OCCUPIED
                self.grav -= self.gravBase

            # if all particles below static, then this particle should be static
            staticLeft = x == 0 or grid[x-1][y-1] == STATIC
            staticBelow = grid[x][y-1] == STATIC
            staticRight = x == len(grid)-1 or grid[x+1][y-1] == STATIC
            if staticLeft and staticBelow and staticRight:
                grid[x][y] = STATIC
        
        if self.grav < 0:
            self.grav = 0
            
        self.grav += self.gravBase


EMPTY = 0
OCCUPIED = 1
STATIC = 2

class SandSimulation:
    width, length = 0, 0
    grid = [[]]
    particles = []

    def __init__(self, width, length):
        self.width = width
        self.length = length
        self.grid = [[EMPTY]*length for _ in range(width)]

    def addSand(self, pos, color):
        part = Particle(self.grid, pos, color)
        self.particles.append(part)


    # step will run a single step in the simulation, where all sand particles will fall if they can
    # will run in order of particles added
    def step(self):
        for part in self.particles:
            part.fall()