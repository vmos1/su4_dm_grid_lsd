# Run SU(4) DM tests
You need two directory paths : Build directory: `build_dir` and Run directory: `run_dir`
## Build executables
- `cd <run_dir>`
- `mkdir build`
- `cd build`
- Copy the contents of the folder `su4_dm_grid_lsd/run_gauge_gen/run_lassen/code/` into `build`: 
  - `cp code/*.cu .`
- Copy the file ```su4_dm_grid_lsd/run_gauge_gen/run_lassen/Makefile``` into `build`: 
  - `cp Makefile .`

- Setup paths:
  - `export GRID_DIR=<build_dir>`
  - `export RUN_DIR=<run_dir>`

### SU(4) 1 flavor with domain wall fermions
#### Build executable
- `source $GRID_DIR/setup_env.sh`
- `make dweofa_HSDM`
(For any of the other executables, run corresponding make command. For example, `make hmc_SDM` )
#### Run executable
- `cd $RUN_DIR/`
- `mkdir run1`
- `cd run1`
- Copy the 2 files `su4_dm_grid_lsd/run_gauge_gen/run_lassen/submit_dwf-hsdm.lsf` and `su4_dm_grid_lsd/run_gauge_gen/run_lassen/code/ip_hmc_mobius.xml` into `run1`:
  - `cp submit_dwf-hsdm.lsf .`
  - `cp ip_hmc_mobius.xml .` 
- Submit the job:  `bsub submit_dwf-hsdm.lsf`
