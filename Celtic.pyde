import math
step = 5
grid = step*8
p = PVector(-240+grid/2,-240)
v = PVector(step,step)
s = p.copy()
d = 1

def setup():
    size(480,480)
    background(255)
    gsize = 480/grid
    stroke(255,0,0)
    for i in range(gsize):
        for j in range(gsize):
            rect(i*grid,j*grid,grid,grid)
    stroke(0)

def draw():
    global p, s, v, d
    translate(240,240)
    scale(1,-1)
    fill(0)
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
        ellipse(p.x,p.y,step,step)
    saveFrame("frames/celtic-####.png")
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
        if s.x > 240:
            print("done")
            noLoop()
