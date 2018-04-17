import config

def Borromean():
    config.xsize = 14
    config.ysize = 5
    config.walls = {
            (0,4,1),
            (6,2,1),
            (6,4,1),
            (10,2,1),
            (10,4,1),
            (5,1,0),
            (2,2,0),
            } # 0 is horizontal, 1 vertical
    config.ignoreCrossings = set()
    config.flags |= 1

def longChain():
    config.xsize = 11
    config.ysize = 4
    config.walls = {
             (10,0,0),
             (6,0,0),
             (2,0,0),
             (0,2,1),
             (8,2,1),
             (4,2,0),
             (5,3,1),
             (3,3,1)
             }
    config.ignoreCrossings = {
                       (3,3),
                       (4,4),
                       (5,3),
                       (4,2)
                       }
    config.flags |= 1
    config.flags |= 2
