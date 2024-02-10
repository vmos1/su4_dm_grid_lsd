# Run SU(4) DM tests
You need two directory paths : Build directory: `build_dir` and Run directory: `run_dir`
## Build executables
- `cd <run_dir>`
- `mkdir build`
- `cd build`
- Copy the contents of the folder 'su4_dm_grid_lsd/run_gauge_gen/run_tioga/code/ 'into `build`: 
  - `cp code/* .`
- Copy the [run_gauge_gen/run_tioga/Makefile](https://github.com/vmos1/su4_dm_grid_lsd/blob/main/run_gauge_gen/run_tioga/Makefile) into `build`: 
  - `cp Makefile .`

- Setup paths:
  - `export GRID_DIR=<build_dir>`
  - `export RUN_DIR=<run_dir>`
### HMC test: 
- `source $GRID_DIR/setup_env.sh`
- `make hmc_SDM`
### DWF test: 
- `source $GRID_DIR/setup_env.sh`
- `make dweofa_HSDM`


## Run Grid

- Setup paths:
  - `export GRID_DIR=<build_dir>`
  - `export RUN_DIR=<run_dir>`

### HMC test:
- `cd $RUN_DIR/`
- `mkdir run1`
- `cd run1`
- Copy the file [submit_1_sdm-4flavor.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/main/run_gauge_gen/run_tioga/submit_1_sdm-4flavor.sh) into `run1`:
  - `cp submit_1_sdm-4flavor.sh .`
- Submit the job `submit_1_sdm-4flavor.sh`

### dwf test
- `cd $RUN_DIR/`
- `mkdir run2`
- `cd run2`
- Copy the file [submit_2_dwfhsdm.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/main/run_gauge_gen/run_tioga/submit_2_dwf-hsdm.sh) into `run2`:
  - `cp submit_2_dwfhsdm.sh .`
- Submit the job `sbatch submit_2_dwfhsdm.sh`
