# sites: Lime, MPFR place in grid_prefix
##################
export grid=$GRID_DIR
export prefix=$GRID_DIR/grid_prefix


mkdir -p $prefix
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
#MPFR : already installed on Tioga
##################

##################
#Obtain Grid and support codes
##################

cd $grid
source setup_env.sh
module list 

git clone https://paboyle@github.com/paboyle/Grid
cd Grid
git checkout -b june15_2023 e3e1cc19620b8ee9834dfb35491ff6c36857d52c
#git checkout -b may11_2023 876c8f4478886479bcd1e505e5481bf34afb8958
#git checkout -b june15_2023 d72e914cf0ed7be6749f13dc307fa0dceaa1add2
./bootstrap.sh

##################
#build Grid
##################
cd $grid/
mkdir -p install/build-Nc4
cd install/build-Nc4

../../Grid/configure --enable-comms=mpi-auto --enable-unified=no --enable-shm=nvlink --enable-accelerator=hip  --enable-gen-simd-width=64  --enable-simd=GPU --enable-Nc=4 --disable-fermion-reps --with-lime=$prefix/lime-1.3.2 --prefix=$prefix CXX=hipcc MPICXX=mpicxx CXXFLAGS="-fPIC -I/opt/rocm-5.2.0/include/ -std=c++17 -I${MPICH_DIR}/include" LDFLAGS="-L${MPICH_DIR}/lib -lmpi -L${CRAY_MPICH_ROOTDIR}/gtl/lib -lamdhip64  -g -ltcmalloc -lmpi_gtl_hsa" HIPFLAGS="--amdgpu-target=gfx90a"

make -j 14 2>&1 | tee op_grid.out
make install
