import math
from Colour import hsl2rgb

step = 5
grid = step*8
p = PVector(-240+grid/2,-240)
v = PVector(step,step)
s = p.copy()
d = 1
PHI = (1 + math.sqrt(5))/2
c = 0
r = True

def setup():
    global img, c
    size(480,480)
    background(255)
    gsize = 480/grid
    img = createGraphics(480,480)
    img.beginDraw()
    img.stroke(0)
    for i in range(gsize):
        for j in range(gsize):
            img.rect(i*grid,j*grid,grid,grid)
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
    gd = ((p.x - grid/4)//(grid/2))%2
    if (gd == d
    or abs(p.x) >= 240 - step 
    or abs(p.y) >= 240 - step 
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
    if abs(p.x) > 240 and p.x * v.x > 0:
        v.x = - v.x
        if p.x > 240:
            p.x = 480 - p.x
        if p.x < -240:
            p.x = -480 - p.x
        d = 1 - d
    if abs(p.y) > 240 and p.y * v.y > 0:
        v.y = - v.y
        if p.y > 240:
            p.y = 480 - p.y
        if p.y < 0:
            p.y = -480 - p.y
        d = 1 - d
    if p == s:
        s.add(PVector(grid,0))
        p = s.copy()
        v = PVector(step,step)
        d = 1 - d
        c += 1
        if s.x > 240:
            r = False
