export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/cray/pe/mpich/8.1.21/gtl/lib/

module load PrgEnv-gnu
module load rocm/5.2.0
module load cray-mpich/8.1.17
#module load gperftools
#module load gmp
module load cray-fftw
module load craype-accel-amd-gfx90a

