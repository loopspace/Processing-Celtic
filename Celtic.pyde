import math
from colour import hsl2rgb
import config
import utils
from links import *
import letters

PHI = (1 + math.sqrt(5))/2
c = 0
r = True

def settings():
    letters.setMessage("celtic")
    
    if config.flags & 1 == 1:
        utils.symmetriseWalls()
    if config.flags & 2 == 2:
        utils.symmetriseIgnores()
    utils.initialiseCrossings()
    size(config.xsize*config.grid,config.ysize*config.grid)
    
def setup():
    global img, p, v, s, u
    p,v = utils.newStrand()
    s = p.copy()
    u = v.copy()
    background(255)
    img = createGraphics(config.xsize*config.grid,config.ysize*config.grid)
    img.beginDraw()
    img.translate(config.xsize*config.grid/2,config.ysize*config.grid/2)
    img.scale(1,-1)
    if config.drawGrid:
        img.stroke(127)
        img.strokeWeight(0)
        for i in range(0,config.xsize):
            for j in range(0,config.ysize):
                img.rect(i*config.grid-config.xsize*config.grid/2,j*config.grid-config.ysize*config.grid/2,config.grid,config.grid)
    if config.drawWalls:
        img.stroke(0)
        img.strokeWeight(3)
        for w in config.walls:
            img.line((w[0]-1+w[2])*config.grid/2,(w[1]-w[2])*config.grid/2,(w[0]+1-w[2])*config.grid/2,(w[1]+w[2])*config.grid/2)
    img.endDraw()
    stroke(0)

def draw():
    global p, s, v, u, c, r
    background(255)
    translate(config.xsize*config.grid/2,config.ysize*config.grid/2)
    scale(1,-1)
    fill(0)
    imageMode(CENTER)
    pushMatrix()
    scale(1,-1)
    image(img,0,0)
    popMatrix()
    if not r:
        if config.recording:
            saveFrame("frames/celtic-####.png")
        print("All done")
        noLoop()
        return

    p.add(v)
    d = PVector(0,0)
    trace = True
    if utils.nearCrossing(p):
        t = utils.crossingType(p)
        if v.x == -t*v.y:
            trace = False
        if t == 0:
            w = utils.getWall(p)
            d.x = -(w[0]*config.grid/2 - p.x)*(1 - w[2])/4
            d.y = -(w[1]*config.grid/2 - p.y)*w[2]/4
    if utils.atCrossing(p):
        gx,gy = utils.getCrossing(p)
        config.crossings[gx][gy] |= int(2**((-v.x+5)/5 + (-v.y+5)/10))
        t = utils.crossingType(p)
        if v.x != t*v.y:
            trace = False
        if t == 0:
            w = utils.getWall(p)
            if w[2] == 1:
                v.x *= -1
            else:
                v.y *= -1
        config.crossings[gx][gy] |= int(2**((v.x+5)/5 + (v.y+5)/10))
    if trace:
        img.beginDraw()
        #img.fill(0)
        img.noStroke()
        img.fill(*hsl2rgb(c*PHI,1,.5))
        img.translate(config.xsize*config.grid/2,config.ysize*config.grid/2)
        img.scale(1,-1)
        img.ellipse(p.x - d.x,p.y - d.y,config.step,config.step)
        img.endDraw()
    ellipse(p.x,p.y,config.step,config.step)
    
    if config.recording:
        saveFrame("frames/celtic-####.png")

    if p == s and v == u:
        p,v = utils.newStrand()
        if not p:
            r = False
        else:
            s = p.copy()
            u = v.copy()
            c += 1
