# Instructions to build Hadrons on Tioga at Livermore
(Note: Hadrons requires Grid to be installed)
- Enter the Grid build directory `build_dir`.
- Copy the scripts `build_grid_hadrons.sh` and `setup_env.sh` from this folder to `build_dir`.
- `export GRID_DIR=<build_dir>`
- Run the script `./build_hadrons_tioga.sh 2>&1 | tee op_hadrons_build.out`
