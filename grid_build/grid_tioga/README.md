# Instructions to build Grid on Tioga at Livermore
- Create a build directory `build_dir`.
- Copy the scripts `build_tioga.sh` and `setup_env.sh` from this [folder](https://github.com/vmos1/su4_dm_grid_lsd/tree/main/grid_build/grid_tioga) to `build_dir`.
- Run the script `./build_tioga.sh`


# Test build
## Grid benchmarks
- Create a run directory `run_dir` and copy the [folder](https://github.com/vmos1/su4_dm_grid_lsd/tree/develop/grid_build/grid_tioga/grid_benchmarks_tests) into it: 
  - `mkdir run_dir`
  - `cd run_dir`
  -  `cp -r grid_benchmarks_tests .`
- Now `cd grid_benchmarks_tests` 
- Edit the contents of each of the 3 files `run_benchmark*.h`:
  - SETUP_DIR=<path to `build_dir` above>
- Now submit the scripts:
  - `sbatch run_benchmark1_1node_dwf_fp32.sh`
  - `sbatch run_benchmark2_2nodes_dwf_fp32.sh`
  - `sbatch run_benchmark3_dwf_ITT.sh`
