import math
from Colour import hsl2rgb

step = 5
grid = step*8
xsize = 14
ysize = 5
PHI = (1 + math.sqrt(5))/2
c = 0
r = True
recording = True
walls = {
         (0,4,1),
         (6,2,1),
         (6,4,1),
         (10,2,1),
         (10,4,1),
         (5,1,0),
         (2,2,0),
         } # 0 is horizontal, 1 vertical

crossings = []
for i in range(2*xsize+1):
    crossings.append([])
    for j in range(2*ysize+1):
        crossings[i].append(0)

for i in range(2*ysize+1):
    crossings[xsize][i] = 8+4
    crossings[-xsize][i] = 2+1
for i in range(2*xsize+1):
    crossings[i][ysize] = 8+2
    crossings[i][-ysize] = 4+1

def symmetriseCrossings():
    a = set()
    for w in walls:
        a.add((w[0],-w[1],w[2]))
        a.add((-w[0],-w[1],w[2]))
        a.add((-w[0],w[1],w[2]))
    for b in a:
        walls.add(b)

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
    if abs(gx) == xsize:
        return 0
    if abs(gy) == ysize:
        return 0
    if gx%2 == 1:
        return 1
    return -1

def getWall(p):
    '''Get the wall at the given crossing.'''
    gx,gy = getCrossing(p)
    if abs(gx) == xsize:
        # Vertical edge
        return [False,False,1]
    if abs(gy) == ysize:
        # Horizontal edge
        return [False,False,0]
    for w in walls:
        if gx == w[0] and gy == w[1]:
            return w
    return False

def newStrand():
    for i in range(len(crossings)):
        x = (i + xsize)%(2*xsize+1) - xsize
        for j in range(len(crossings[i])):
            y = (j + ysize)%(2*ysize+1) - ysize
            if (x + xsize + y + ysize)%2 == 1:
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
    symmetriseCrossings()
    global img, p, v, s, u
    p,v = newStrand()
    s = p.copy()
    u = v.copy()
    size(xsize*grid,ysize*grid)
    background(255)
    img = createGraphics(xsize*grid,ysize*grid)
    img.beginDraw()
    img.translate(xsize*grid/2,ysize*grid/2)
    img.scale(1,-1)
    img.stroke(127)
    img.strokeWeight(0)
    for i in range(0,xsize):
        for j in range(0,ysize):
            img.rect(i*grid-xsize*grid/2,j*grid-ysize*grid/2,grid,grid)
    img.stroke(0)
    img.strokeWeight(3)
    for w in walls:
        img.line((w[0]-1+w[2])*grid/2,(w[1]-w[2])*grid/2,(w[0]+1-w[2])*grid/2,(w[1]+w[2])*grid/2)
    img.endDraw()
    stroke(0)

def draw():
    global p, s, v, u, c, r
    background(255)
    translate(xsize*grid/2,ysize*grid/2)
    scale(1,-1)
    fill(0)
    imageMode(CENTER)
    pushMatrix()
    scale(1,-1)
    image(img,0,0)
    popMatrix()
    if not r:
        if recording:
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
        img.translate(xsize*grid/2,ysize*grid/2)
        img.scale(1,-1)
        img.ellipse(p.x,p.y,step,step)
        img.endDraw()
    ellipse(p.x,p.y,step,step)
    
    if recording:
        saveFrame("frames/celtic-####.png")

    if p == s and v == u:
        p,v = newStrand()
        if not p:
            r = False
        else:
            s = p.copy()
            u = v.copy()
            c += 1
