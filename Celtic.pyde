import math
from Colour import hsl2rgb

step = 5
grid = step*8
edge = 240/grid
p = PVector(-240+grid/2,-240)
v = PVector(step,step)
s = p.copy()
d = 1
PHI = (1 + math.sqrt(5))/2
c = 0
r = True
walls = [(1,0,1)] # 0 is horizontal, 1 vertical

def checkWalls(p):
    gx = (p.x + grid/4)//(grid/2)
    gy = (p.y + grid/4)//(grid/2)
    if abs(gx) == 2*edge: # Vertical edge
        return 1
    if abs(gy) == 2*edge: # Horizontal edge
        return -1
    for w in walls:
        if w[2] == 0: # Horizontal wall
            if gx == w[0]*2 + 1 and gy == w[1]*2:
                return -1
        else: # Vertical wall
            if gx == w[0]*2 and gy == w[1]*2 + 1:
                return 1
    return 0

def setup():
    global img, c
    size(480,480)
    background(255)
    gsize = 480/grid
    img = createGraphics(480,480)
    img.beginDraw()
    img.translate(240,240)
    img.scale(1,-1)
    img.stroke(127)
    for i in range(-gsize/2,gsize/2):
        for j in range(-gsize/2,gsize/2):
            img.rect(i*grid,j*grid,grid,grid)
    img.stroke(0)
    img.strokeWeight(3)
    for w in walls:
        img.line(w[0]*grid,w[1]*grid,(w[0]+1-w[2])*grid,(w[1]+w[2])*grid)
    img.endDraw()
    stroke(0)

def draw():
    global p, s, v, d, c, r
    background(255)
    translate(240,240)
    scale(1,-1)
    fill(0)
    imageMode(CENTER)
    pushMatrix()
    scale(1,-1)
    image(img,0,0)
    popMatrix()
    w = checkWalls(p)
    gd = ((p.x + grid/4)//(grid/2))%2
    if ((w == 0 and gd == d)
        or (w != 0 and (p.x%grid == step or p.x%grid == grid - step or p.y%grid == step or p.y%grid == grid - step))
        or (p.x%grid != 0
        and p.y%grid != 0 
        and p.x%grid != step
        and p.x%grid != grid - step
        and p.y%grid != step    
        and p.y%grid != grid - step)):
        img.beginDraw()
        #img.fill(0)
        img.noStroke()
        img.fill(*hsl2rgb(c*PHI,1,.5))
        img.translate(240,240)
        img.scale(1,-1)
        img.ellipse(p.x,p.y,step,step)
        img.endDraw()
    
    ellipse(p.x,p.y,step,step)
    #saveFrame("frames/celtic-####.png")
    if not r:
        print("done")
        noLoop()
    p.add(v)
    w = checkWalls(p)
    if p.x%grid == 0 and w == 1:
        # vertical bounce, flip horizontal velocity
        v.x = -v.x
        d = 1 - d
    elif p.y%grid == 0 and w == -1:
        # horizontal bounce, flip vertical velocity
        v.y = -v.y
        d = 1 - d
    if p == s:
        s.add(PVector(grid,0))
        p = s.copy()
        v = PVector(step,step)
        d = ((p.x + grid/4)//(grid/2))%2
        c += 1
        if s.x > 240:
            r = False
