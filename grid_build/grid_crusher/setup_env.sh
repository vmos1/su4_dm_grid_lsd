export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/gcc-11.2.0/gperftools-2.9.1-72ubwtuc5wcz2meqltbfdb76epufgzo2/lib
module load emacs 
module load PrgEnv-gnu
module load rocm/5.2.0
module load cray-mpich/8.1.17
module load gmp
module load fftw
#module load cray-fftw
#module load gperftools
module load craype-accel-amd-gfx90a
export LD_LIBRARY_PATH=/opt/gcc/mpfr/3.1.4/lib:$LD_LIBRARY_PATH
