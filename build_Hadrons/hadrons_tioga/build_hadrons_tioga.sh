##################
export grid=$GRID_DIR
export prefix=$GRID_DIR/grid_prefix
export build=$grid/hadrons_build
#################
cd $grid

source setup_env.sh
git clone git@github.com:aportelli/Hadrons.git

cd Hadrons
./bootstrap.sh

mkdir $build
cd $build

../Hadrons/configure --prefix=$prefix  --with-grid=$prefix

make -j 14 
make install
