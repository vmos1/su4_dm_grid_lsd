
## Setup conda environment
Use anaconda and the file `requirements.txt`


## Commands to setup directories for runs 


- Fresh run: 

``` python 1_setup_hmc.py -r fresh -d <directory_location> -m tioga ```

- Extend run: 

``` python 1_setup_hmc.py -r extend -d <run_dir> -m tioga ```


- Checkpoint start run : 

``` python 1_setup_hmc.py -r checkpoint_start -d <directory_location> -m tioga -c <config_file_location> ```
