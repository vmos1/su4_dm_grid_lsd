
# sites: Lime, MPFR place in $HOME/prefix
##################
export grid=$GRID_DIR
export prefix=$GRID_DIR/grid_prefix

mkdir -p $prefix
mkdir -p $grid
echo GRID $grid
echo PREFIX $prefix

##################
#LIME
##################
cd $prefix
wget http://usqcd-software.github.io/downloads/c-lime/lime-1.3.2.tar.gz
tar xvzf lime-1.3.2.tar.gz
cd lime-1.3.2
./configure --prefix $prefix
make all install 2>&1 | tee op_lime.out

##################
#MPFR
##################
cd $prefix
wget https://www.mpfr.org/mpfr-current/mpfr-4.2.0.tar.gz
tar xvzf mpfr-4.2.0.tar.gz
cd mpfr-4.2.0
echo $OLCF_GMP_ROOT

#./configure --prefix $prefix --with-gmp=/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/cce-14.0.0/gmp-6.2.1-gw47mfuvanwrvrh3rj6qrjz6hpey7423/
#./configure --prefix $prefix --with-gmp=/sw/crusher/spack-envs/base/opt/cray-sles15-zen2/gcc-11.2.0/gmp-6.2.1-idotvdzakdbt5mdfbxiffbln672cifcz
./configure --prefix $prefix --with-gmp=$OLCF_GMP_ROOT

make all install 2>&1 | tee op_mpfr.out

##################
#Obtain Grid and support codes
##################

cd $grid
source setup_env.sh
git clone https://paboyle@github.com/paboyle/Grid
cd Grid
./bootstrap.sh

##################
#build Grid
##################
cd $grid/
mkdir -p install/build-Nc4
cd install/build-Nc4

#../../Grid/configure --enable-comms=mpi-auto --enable-unified=no --enable-shm=nvlink --enable-accelerator=hip  --enable-gen-simd-width=64 --enable-simd=GPU --enable-Nc=4  --with-gmp=/sw/crusher/spack-envs/base/opt/cray-sles15-zen2/gcc-11.2.0/gmp-6.2.1-idotvdzakdbt5mdfbxiffbln672cifcz --with-mpfr=/opt/cray/pe/gcc/mpfr/3.1.4/ --with-fftw=/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/gcc-11.2.0/fftw-3.3.9-3hxcnpeqmrvidsb3erk36wi75kexaznd  --disable-fermion-reps  --prefix=$prefix CXX=hipcc MPICXX=mpicxx CXXFLAGS="-fPIC -I/opt/rocm-5.2.0/include/ -std=c++14 -I${MPICH_DIR}/include  -g"

../../Grid/configure --enable-comms=mpi-auto --enable-unified=no --enable-shm=nvlink --enable-accelerator=hip  --enable-gen-simd-width=64 --enable-simd=GPU --enable-Nc=4  --with-gmp=$OLCF_GMP_ROOT --with-fftw=/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/gcc-11.2.0/fftw-3.3.9-3hxcnpeqmrvidsb3erk36wi75kexaznd  --disable-fermion-reps  --prefix=$prefix CXX=hipcc MPICXX=mpicxx CXXFLAGS="-fPIC -I/opt/rocm-5.2.0/include/ -std=c++14 -I${MPICH_DIR}/include -g" LDFLAGS="-L${MPICH_DIR}/lib -lmpi -L${CRAY_MPICH_ROOTDIR}/gtl/lib -lamdhip64"

make -j 14 2>&1 | tee op_grid.out
make install
