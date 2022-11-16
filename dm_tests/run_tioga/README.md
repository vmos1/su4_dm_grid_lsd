# Run SU(4) DM tests

## Build executables
- `mkdir dm_tests/build`
- `cd dm_tests/build`
- Copy the contents of the folder [`dm_tests/code`](https://github.com/vmos1/su4_dm_grid_lsd/tree/develop/dm_tests/code) into `build`: 
  - `cp code/* .`
- Copy the [dm_tests/run_tioga/Makefile](https://github.com/vmos1/su4_dm_grid_lsd/blob/develop/dm_tests/run_tioga/Makefile) into it: 
  - `cp Makefile .`
## Run Grid
### HMC test:
- cd `dm_tests/build`
- `make hmc_SDM`
- `cd ..`
- `mkdir run1`
- `cd run1`
- Copy the file [submit1.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/develop/dm_tests/run_tioga/submit.sh) into `run1`.
- Submit the job `sbatch submit1.sh`

### dwf test
- `make dweofa_HSDM`
