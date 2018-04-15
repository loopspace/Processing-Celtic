import math
from Colour import hsl2rgb

step = 5
grid = step*8
edge = 240/grid
PHI = (1 + math.sqrt(5))/2
c = 0
r = True
walls = [
         (3,0,1),
         (0,3,0),
         (-3,0,1),
         (0,-3,0),
         (7,0,1),
         (0,7,0),
         (-7,0,1),
         (0,-7,0),
         (7,4,1),
         (4,7,0),
         (-7,4,1),
         (4,-7,0),
         (7,-4,1),
         (-4,7,0),
         (-7,-4,1),
         (-4,-7,0)
         ] # 0 is horizontal, 1 vertical

crossings = []
for i in range(4*edge+1):
    crossings.append([])
    for j in range(4*edge+1):
        crossings[i].append(0)

for i in range(4*edge+1):
    crossings[2*edge][i] = 8+4
    crossings[-2*edge][i] = 2+1
    crossings[i][2*edge] = 8+2
    crossings[i][-2*edge] = 4+1

def nearCrossing(p):
    '''Are we plus or minus 1 from a crossing?'''
    x = p.x%(grid/2)
    y = p.y%(grid/2)
    if x == step or x == grid/2 - step or y == step or y == grid/2 - step:
        return True
    return False

def atCrossing(p):
    '''Are we at a crossing?'''
    x = p.x%(grid/2)
    y = p.y%(grid/2)
    if x == 0 or y == 0:
        return True
    return False
    
def getCrossing(p):
    '''Get the nearest half-grid coordinate.'''
    return int((p.x + grid/4)//(grid/2)), int((p.y + grid/4)//(grid/2))

def crossingType(p):
    '''Get the crossing type of the nearest half-grid coordinate.
    Returns 0 for a wall, 1 for main diagonal over, -1 for a under.'''
    w = getWall(p)
    if w:
        return 0
    gx,gy = getCrossing(p)
    if abs(gx) == 2*edge:
        return 0
    if abs(gy) == 2*edge:
        return 0
    if gx%2 == 1:
        return 1
    return -1

def getWall(p):
    '''Get the wall at the given crossing.'''
    gx,gy = getCrossing(p)
    if abs(gx) == 2*edge:
        # Vertical edge
        return [False,False,1]
    if abs(gy) == 2*edge:
        # Horizontal edge
        return [False,False,0]
    for w in walls:
        if gx == w[0] and gy == w[1]:
            return w
    return False

def newStrand():
    for i in range(len(crossings)):
        x = (i + 2*edge)%(4*edge+1) - 2*edge
        for j in range(len(crossings[i])):
            y = (j + 2*edge)%(4*edge+1) - 2*edge
            if (x + y)%2 == 1:
                if crossings[i][j] != 15:
                    p = PVector(x * grid/2, y * grid/2)
                    a = crossings[i][j]
                    if crossings[i][j] & 1 != 1:
                        v = PVector(-5,-5)
                        crossings[i][j] |= 1
                    elif crossings[i][j] & 2 != 2:
                        v = PVector(-5,5)
                        crossings[i][j] |= 2
                    elif crossings[i][j] & 4 != 4:
                        v = PVector(5,-5)
                        crossings[i][j] |= 4
                    elif crossings[i][j] & 8 != 8:
                        v = PVector(5,5)
                        crossings[i][j] |= 8
                    return p,v
    return False, False

def setup():
    global img, p, v, s, u
    p,v = newStrand()
    s = p.copy()
    u = v.copy()
    size(480,480)
    background(255)
    gsize = 480/grid
    img = createGraphics(480,480)
    img.beginDraw()
    img.translate(240,240)
    img.scale(1,-1)
    img.stroke(127)
    img.strokeWeight(0)
    for i in range(-gsize/2,gsize/2):
        for j in range(-gsize/2,gsize/2):
            img.rect(i*grid,j*grid,grid,grid)
    img.stroke(0)
    img.strokeWeight(3)
    for w in walls:
        img.line((w[0]-1+w[2])*grid/2,(w[1]-w[2])*grid/2,(w[0]+1-w[2])*grid/2,(w[1]+w[2])*grid/2)
    img.endDraw()
    stroke(0)

def draw():
    global p, s, v, u, c, r
    background(255)
    translate(240,240)
    scale(1,-1)
    fill(0)
    imageMode(CENTER)
    pushMatrix()
    scale(1,-1)
    image(img,0,0)
    popMatrix()
    if not r:
        saveFrame("frames/celtic-####.png")
        print("All done")
        noLoop()
        return

    p.add(v)
    trace = True
    if nearCrossing(p):
        t = crossingType(p)
        if v.x == -t*v.y:
            trace = False
    if atCrossing(p):
        gx,gy = getCrossing(p)
        crossings[gx][gy] |= int(2**((-v.x+5)/5 + (-v.y+5)/10))
        t = crossingType(p)
        if v.x != t*v.y:
            trace = False
        if t == 0:
            w = getWall(p)
            if w[2] == 1:
                v.x *= -1
            else:
                v.y *= -1
        crossings[gx][gy] |= int(2**((v.x+5)/5 + (v.y+5)/10))
    if trace:
        img.beginDraw()
        #img.fill(0)
        img.noStroke()
        img.fill(*hsl2rgb(c*PHI,1,.5))
        img.translate(240,240)
        img.scale(1,-1)
        img.ellipse(p.x,p.y,step,step)
        img.endDraw()
    ellipse(p.x,p.y,step,step)

    saveFrame("frames/celtic-####.png")

    if p == s and v == u:
        p,v = newStrand()
        if not p:
            r = False
        else:
            s = p.copy()
            u = v.copy()
            c += 1
