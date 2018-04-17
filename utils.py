import math
import config

def initialiseCrossings():
    for i in range(2*config.xsize+1):
        config.crossings.append([])
        for j in range(2*config.ysize+1):
            config.crossings[i].append(0)
    
    for i in range(2*config.ysize+1):
        config.crossings[config.xsize][i] = 8+4
        config.crossings[-config.xsize][i] = 2+1
    for i in range(2*config.xsize+1):
        config.crossings[i][config.ysize] = 8+2
        config.crossings[i][-config.ysize] = 4+1
    
def symmetriseWalls():
    a = set()
    for w in config.walls:
        a.add((w[0],-w[1],w[2]))
        a.add((-w[0],-w[1],w[2]))
        a.add((-w[0],w[1],w[2]))
    for b in a:
        config.walls.add(b)

def symmetriseIgnores():
    a = set()
    for i in config.ignoreCrossings:
        a.add((i[0],-i[1]))
        a.add((-i[0],-i[1]))
        a.add((-i[0],i[1]))
    for b in a:
        config.ignoreCrossings.add(b)

def nearCrossing(p):
    '''Are we plus or minus 1 from a crossing?'''
    x = p.x%(config.grid/2)
    y = p.y%(config.grid/2)
    if x == config.step or x == config.grid/2 - config.step or y == config.step or y == config.grid/2 - config.step:
        return True
    return False

def atCrossing(p):
    '''Are we at a crossing?'''
    x = p.x%(config.grid/2)
    y = p.y%(config.grid/2)
    if x == 0 or y == 0:
        return True
    return False
    
def getCrossing(p):
    '''Get the nearest half-grid coordinate.'''
    return int((p.x + config.grid/4)//(config.grid/2)), int((p.y + config.grid/4)//(config.grid/2))

def crossingType(p):
    '''Get the crossing type of the nearest half-grid coordinate.
    Returns 0 for a wall, 1 for main diagonal over, -1 for a under.'''
    w = getWall(p)
    if w:
        return 0
    gx,gy = getCrossing(p)
    if abs(gx) == config.xsize:
        return 0
    if abs(gy) == config.ysize:
        return 0
    if gx%2 == 1:
        return 1
    return -1

def getWall(p):
    '''Get the wall at the given crossing.'''
    gx,gy = getCrossing(p)
    if abs(gx) == config.xsize:
        # Vertical edge
        return [gx,gy,1]
    if abs(gy) == config.ysize:
        # Horizontal edge
        return [gx,gy,0]
    for w in config.walls:
        if gx == w[0] and gy == w[1]:
            return w
    return False

def newStrand():
    for i in range(len(config.crossings)):
        x = (i + config.xsize)%(2*config.xsize+1) - config.xsize
        for j in range(len(config.crossings[i])):
            y = (j + config.ysize)%(2*config.ysize+1) - config.ysize
            if (x + config.xsize + y + config.ysize)%2 == 1:
                if config.crossings[i][j] != 15 and not (x,y) in config.ignoreCrossings:
                    p = PVector(x * config.grid/2, y * config.grid/2)
                    a = config.crossings[i][j]
                    if config.crossings[i][j] & 1 != 1:
                        v = PVector(-5,-5)
                        config.crossings[i][j] |= 1
                    elif config.crossings[i][j] & 2 != 2:
                        v = PVector(-5,5)
                        config.crossings[i][j] |= 2
                    elif config.crossings[i][j] & 4 != 4:
                        v = PVector(5,-5)
                        config.crossings[i][j] |= 4
                    elif config.crossings[i][j] & 8 != 8:
                        v = PVector(5,5)
                        config.crossings[i][j] |= 8
                    return p,v
    return False, False
