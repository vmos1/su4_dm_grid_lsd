# Run SU(4) DM tests

## Build executables
- `mkdir dm_tests/build`
- `cd dm_tests/build`
- Copy the contents of the folder [`dm_tests/code`](https://github.com/vmos1/su4_dm_grid_lsd/tree/develop/dm_tests/code) into `build`: 
  - `cp code/* .`
- Copy the [dm_tests/run_tioga/Makefile](https://github.com/vmos1/su4_dm_grid_lsd/blob/develop/dm_tests/run_tioga/Makefile) into `build`: 
  - `cp Makefile .`
- Edit the submit script:
  - `GRID=<path to build directory for Grid>`
  - `PREFIX=<path to build directory for Grid>/grid_prefix`
  
## Run Grid
### HMC test:
- `cd dm_tests/build`
- `source {build_dir}/setup_env.sh`
- `make hmc_SDM`
- `cd ..`
- `mkdir run1`
- `cd run1`
- Copy the file [submit.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/main/dm_tests/run_tioga/submit.sh) into `run1`:
  - `cp submit.sh .`
- Edit the submit script:
  - `GRID=<path to build directory for Grid>`
- Submit the job `sbatch submit1.sh`

### dwf test
- `cd dm_tests/build`
- `source {build_dir}/setup_env.sh`
- `make dweofa_HSDM`
- `cd ..`
- `mkdir run2`
- `cd run2`
- Copy the file [submit2.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/main/dm_tests/run_tioga/submit2.sh) into `run2`:
  - `cp submit2.sh .`
- Edit the submit script:
  - `GRID=<path to build directory for Grid>`
- Submit the job `sbatch submit2.sh`
