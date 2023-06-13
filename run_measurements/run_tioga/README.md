# Run analysis code for generated gauge configurations
You need two directory paths : Build directory: `build_dir` and Run directory: `run_dir`
- Need a gauge config file with name `ckpoint_lat_16_8.140`
- Edit the xml file `DWFtest.xm` and link appropriate gauge config file in lines 5 and 28.

## Run Hadrons
- Setup paths:
  - `export GRID_DIR=<build_dir>`
  - `export RUN_DIR=<run_dir>`

### dwf test
- `cd $RUN_DIR`
- `mkdir measurement`
- `cd measurement`
- Copy the file [TestHadrons.sh](https://github.com/vmos1/su4_dm_grid_lsd/blob/main/run_measurements/run_tioga/TestHadrons.sh) into this directory:
  - `cp TestHadrons.sh .`
- Submit the job `sbatch TestHadrons.sh`