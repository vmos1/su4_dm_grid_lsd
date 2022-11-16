# Run SU(4) DM tests

## Build executables
- `mkdir dm_tests/build`
- Copy the contents of the folder [fldr](https://github.com/vmos1/su4_dm_grid_lsd/tree/develop/dm_tests/code) into `build`: 
  - `cp code/* dm_tests/build`
- Copy the [Makefile]() into it: `cp Makefile .`
## Run Grid
### HMC test:
- cd `dm_tests/build`
- `make hmc_SDM`
- `cd ..`
- `mkdir dm_tests/run1`
- Copy the file [submit1.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/develop/dm_tests/run_tioga/submit.sh) into `run1`.
- Submit the job `sbatch submit1.sh`

### dwf test
- `make dweofa_HSDM`
