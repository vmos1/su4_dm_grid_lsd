# Instructions to build Hadrons on Tioga at Livermore
(Note: Hadrons requires Grid to be installed)
- Enter the Grid build directory `build_dir`.
- Copy the scripts `build_grid_hadrons.sh` and `setup_env.sh` from this [folder](https://github.com/vmos1/su4_dm_grid_lsd/tree/main/hadrons_build/hadrons_tioga) to `build_dir`.
- `export GRID_DIR=<build_dir>`
- Run the script `./build_hadrons_tioga.sh 2>&1 | tee op_hadrons_build.out`

# Test build
## Grid benchmarks
- Create a run directory `run_dir` and copy the folder [grid_benchmarks_tests](https://github.com/vmos1/su4_dm_grid_lsd/tree/main/grid_build/grid_tioga/grid_benchmarks_tests) into it: 
  - `mkdir run_dir`
  - `cd run_dir`
  - `cp -r grid_benchmarks_tests .`
  - `cd grid_benchmarks_tests` 
- Setup variables:
  - `export GRID_DIR=<build_dir>`
  - `export RUN_DIR=<run_dir>`
- Now submit the scripts:
  - `sbatch run_benchmark1_1node_dwf_fp32.sh`
  - `sbatch run_benchmark2_2nodes_dwf_fp32.sh`
  - `sbatch run_benchmark3_dwf_ITT.sh`
