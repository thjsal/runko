#pragma once

#include <vector>
#include <string>

#include "namer.h"
#include "../corgi/corgi.h"
#include "../tools/mesh.h"
#include "../pic/particle.h"
#include "../pic/tile.h"


namespace h5io { 


template<size_t D>
class TestPrtclWriter {

  private:

    /// general file extension to be appended to file names
    const string extension = ".h5";
    
    /// Object to handle file names and extensions
    std::string fname;

    /// meshes
    std::vector< toolbox::Mesh<double> > arrs;

    /// mpi receive buffer
    std::vector< toolbox::Mesh<double> > rbuf;

    // temporary test arrays
    std::vector< toolbox::Mesh<int> > arrs2;
    std::vector< toolbox::Mesh<int> > rbuf2;

    /// internal image size
    int nx,ny,nz;


  public:

    /// particle species/container to read/write
    int ispc = 0;

    /// data stride length
    int stride = 1;

    /// constructor that creates a name and opens the file handle
    TestPrtclWriter(
        const std::string& prefix, 
        int Nx, int NxMesh,
        int Ny, int NyMesh,
        int Nz, int NzMesh,
        int ppc, int n_local_tiles,
        int n_test_particles_approx);


    /// read tile meshes into memory
    void read_tiles(corgi::Node<D>& grid);

    /// communicate snapshots with a B-tree cascade to rank 0
    void mpi_reduce_snapshots(corgi::Node<D>& grid);

    /// write hdf5 file
    bool write(corgi::Node<D>& grid, int lap);
};


} // end of namespace h5io

