import unittest

import sys
sys.path.append('python')
import numpy as np

import pyplasma as plasma


class Conf:

    Nx = 3
    Ny = 3
    Nz = 1

    NxMesh = 3
    NyMesh = 3
    NzMesh = 3

    xmin = 0.0
    xmax = 1.0

    ymin = 0.0
    ymax = 1.0

    #def __init__(self):
    #    print("initialized...")


#load cells into each node
def loadCells(n):
    for i in range(n.getNx()):
        for j in range(n.getNy()):
            if n.getMpiGrid(i,j) == n.rank:
                c = plasma.PlasmaCell(i, j, n.rank, n.getNx(), n.getNy(), 3, 3, 3)
                #c = plasma.VlasovCell(i, j, n.rank, n.getNx(), n.getNy(), 3, 3)
                n.addCell(c) #TODO load data to cell


def wrap(ii, N):
    if ii < 0:
        ii = N-1
        return N-1
    if ii == N:
        return 0
    return ii


class Communications(unittest.TestCase):

    """ Load cells, put running values in to them,
        update boundaries, check that every cell
        has correct boundaries.
    """
    def test_updateBoundaries(self):

        conf = Conf()

        node = plasma.Grid(conf.Nx, conf.Ny)
        node.setGridLims(conf.xmin, conf.xmax, conf.ymin, conf.ymax)

        loadCells(node)

        # lets put values into Yee lattice
        val = 1.0
        for i in range(node.getNx()):
            for j in range(node.getNy()):
                #if n.getMpiGrid(i,j) == n.rank:
                if True:
                    c = node.getCellPtr(i,j)
                    yee = c.getYee(0)

                    for q in range(conf.NxMesh):
                        for k in range(conf.NyMesh):
                            for r in range(conf.NzMesh):
                                yee.ex[q,k,r] = val
                                yee.ey[q,k,r] = val
                                yee.ez[q,k,r] = val

                                yee.bx[q,k,r] = val
                                yee.by[q,k,r] = val
                                yee.bz[q,k,r] = val
                                val += 1

        data = np.zeros((conf.Nx*conf.NxMesh, conf.Ny*conf.NyMesh, conf.Nz*conf.NzMesh, 6))

        for cid in node.getCellIds():
            c = node.getCellPtr( cid )
            (i, j) = c.index()

            yee = c.getYee(0)

            for k in range(conf.NyMesh):
                for q in range(conf.NxMesh):
                    for r in range(conf.NzMesh):
                        data[ i*conf.NxMesh + q, j*conf.NyMesh + k, 0*conf.NzMesh + r, 0] = yee.ex[q,k,r]
                        data[ i*conf.NxMesh + q, j*conf.NyMesh + k, 0*conf.NzMesh + r, 1] = yee.ey[q,k,r]
                        data[ i*conf.NxMesh + q, j*conf.NyMesh + k, 0*conf.NzMesh + r, 2] = yee.ez[q,k,r]
                        data[ i*conf.NxMesh + q, j*conf.NyMesh + k, 0*conf.NzMesh + r, 3] = yee.bx[q,k,r]
                        data[ i*conf.NxMesh + q, j*conf.NyMesh + k, 0*conf.NzMesh + r, 4] = yee.by[q,k,r]
                        data[ i*conf.NxMesh + q, j*conf.NyMesh + k, 0*conf.NzMesh + r, 5] = yee.bz[q,k,r]

        print("r=0-------")
        print(data[:,:,0,0])
        print("r=1-------")
        print(data[:,:,1,0])
        print("r=2-------")
        print(data[:,:,2,0])

        #update boundaries
        for cid in node.getCellIds():
            c = node.getCellPtr( cid )
            c.updateBoundaries(node)

        ref = np.zeros((conf.Nx*conf.Ny*conf.Nz, conf.Nx*conf.NxMesh, conf.Ny*conf.NyMesh, conf.Nz*conf.NzMesh))

        m = 0
        for cid in node.getCellIds():
            c = node.getCellPtr( cid )
            (i, j) = c.index()
            yee = c.getYee(0)

            for k in range(-1, conf.NyMesh+1, 1):
                for q in range(-1, conf.NxMesh+1, 1):
                    for r in range(-1, conf.NzMesh+1, 1):
                        qq = wrap( i*conf.NxMesh + q, conf.Nx*conf.NxMesh )
                        kk = wrap( j*conf.NyMesh + k, conf.Ny*conf.NyMesh )
                        rr = wrap( 0*conf.NzMesh + r, conf.Nz*conf.NzMesh )
                        ref[m, qq, kk, rr] = yee.ex[q,k,r]
            m += 1

        print("cid = 0")
        print(ref[0,:,:,0])
        print(ref[0,:,:,1])
        print(ref[0,:,:,2])

        for m in range(conf.Nx*conf.Ny):
            for i in range(conf.Nx*conf.NxMesh):
                for j in range(conf.Ny*conf.NyMesh):
                    for k in range(conf.Nz*conf.NzMesh):
                        if ref[m,i,j,k] == 0:
                            continue

                        #loop over ex, ey, ez,...
                        for tp in range(5):
                            self.assertEqual( ref[m,i,j,k], data[i,j,k,tp] )
                



