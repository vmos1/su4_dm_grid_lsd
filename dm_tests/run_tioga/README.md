# Run SU(4) DM tests
You need two directory paths : Build directory: `build_dir` and Run directory: `run_dir`
## Build executables
- Setup paths:
  - `export GRID_DIR=<build_dir>`
  - `export RUN_DIR=<run_dir>`
- `mkdir dm_tests/build`
- `cd dm_tests/build`
- Copy the contents of the folder [`dm_tests/code`](https://github.com/vmos1/su4_dm_grid_lsd/tree/develop/dm_tests/code) into `build`: 
  - `cp code/* .`
- Copy the [dm_tests/run_tioga/Makefile](https://github.com/vmos1/su4_dm_grid_lsd/blob/develop/dm_tests/run_tioga/Makefile) into `build`: 
  - `cp Makefile .`

### HMC test: 
- `source $GRID_DIR/setup_env.sh`
- `make hmc_SDM`
### DWF test: 
- `source $GRID_DIR/setup_env.sh`
- `make dweofa_HSDM`
## Run Grid
### HMC test:
- `cd <run_dir>/dm_tests`
- `mkdir run1`
- `cd run1`
- Copy the file [submit1.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/main/dm_tests/run_tioga/submit1.sh) into `run1`:
  - `cp submit1.sh .`
- Submit the job `sbatch submit1.sh`

### dwf test
- `cd <run_dir>/dm_tests`
- `mkdir run2`
- `cd run2`
- Copy the file [submit2.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/main/dm_tests/run_tioga/submit2.sh) into `run2`:
  - `cp submit2.sh .`
- Submit the job `sbatch submit2.sh`
