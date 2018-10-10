try:
    import matplotlib.pyplot as plt
    from matplotlib import cm
    import palettable as pal
    palette = pal.wesanderson.Moonrise1_5.mpl_colormap
except:
    pass

import numpy as np
import random


from visualize import plotNode
from visualize import plotTileBoundaries


class Particles:
    xs  = []
    ys  = []
    zs  = []

    uxs = []
    uys = []
    uzs = []

    def clear(self):
        self.xs  = []
        self.ys  = []
        self.zs  = []

        self.uxs = []
        self.uys = []
        self.uzs = []

def get_particles(node, conf):
    prtcl = Particles()
    prtcl.clear()

    for i in range(conf.Nx):
        for j in range(conf.Ny):
            for k in range(conf.Nz):
                cid = node.id(i,j)
                c = node.getTile(cid)

                x, y, z, ux, uy, uz = get_particles_from_tile(c)

                prtcl.xs.extend(x)
                prtcl.ys.extend(y)
                prtcl.zs.extend(z)

                prtcl.uxs.extend(ux)
                prtcl.uys.extend(uy)
                prtcl.uzs.extend(uz)

    return prtcl


def get_particles_from_tile(tile, ispcs=0):
    container = tile.get_container(ispcs)
    x  = container.loc(0)
    y  = container.loc(1)
    z  = container.loc(2)

    ux = container.vel(0)
    uy = container.vel(1)
    uz = container.vel(2)

    return x, y, z, ux, uy, uz



def plot2dParticles(ax, n, conf, downsample=0):

    #ax.clear()
    ax.cla()
    plotNode(ax, n, conf)
    plotTileBoundaries(ax, n, conf)

    prtcl = get_particles(n, conf)
    Np = len(prtcl.xs)
    #print("particles to plot: {}".format(Np))

    if downsample > 0:
        rindxs = random.sample( range(0, Np-1), int(downsample*Np) )

        prtcl.xs = np.array( prtcl.xs )
        prtcl.ys = np.array( prtcl.ys ) 
        prtcl.zs = np.array( prtcl.zs )

        prtcl.xs = prtcl.xs[rindxs]
        prtcl.ys = prtcl.ys[rindxs]
        prtcl.zs = prtcl.zs[rindxs]

    ax.plot(prtcl.xs, prtcl.ys, ".", color='red')
    










