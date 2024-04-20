
import numpy as np
import os
import argparse
import subprocess as sp
import shutil
import glob

import yaml
from datetime import datetime


def f_write_config(input_dict,fname):
    '''
    Write config file input.yaml
    '''
    with open(fname,'w') as f:
        yaml.dump(input_dict,f,sort_keys=False)
        
def f_read_config(fname):
    '''
    Read from config file input.yaml
    '''
    with open(fname,'r') as f:
        config_dict=yaml.load(f, Loader=yaml.SafeLoader)
        
    return config_dict

def f_get_last_checkpoint(run_dir):
    '''
    Look through saved config files and find last saved configuration number
    '''
    
    assert os.path.exists(run_dir), "run dir doesn't exist %s"%(run_dir)
    checkpt_list=np.sort([int(i.split('/')[-1].split('_lat.')[-1]) for i in glob.glob(run_dir+'/ckpoint_lat*')])

    return checkpt_list[-1]


def f_get_out_filename(run_dir):
    '''
    Get the right file name for output such as  HSDM1.out, HSDM2.out , etc. based on existing files from extensions
    '''
    
    assert os.path.exists(run_dir), "run dir doesn't exist %s"%(run_dir)
    op_suffix=np.sort([int(i.split('/HSDM')[-1].split('.out')[0]) for i in glob.glob(run_dir+'/HSDM*.out')])

    new_suffix=op_suffix[-1]+1 ## Add one to suffix
    new_op_file='HSDM%s.out'%(new_suffix)
    
    return new_op_file

def f_get_xml_file_name(run_type,run_dir):
    
    if run_type=='extend':    
        num_runs=len(glob.glob(run_dir+'*.xml'))
        xml_fname='ip_hmc_mobius_%s.xml'%(num_runs+1)
        ## Ensure you don't overwrite existing xml file
        assert not os.path.isfile(run_dir+xml_fname), "XML file already exists %s"%(run_dir+xml_fname)

    elif run_type in ['fresh','checkpoint_start']:
        xml_fname='ip_hmc_mobius.xml'
        
    return run_dir+'/'+xml_fname


def f_create_seed_string(mode='timestamp'):
    '''
    Create seed strings
    '''
    
    if mode=='timestamp':
        seed=int(datetime.now().timestamp())
        # print(seed)
        
        # Set seed for numpy random number generator
        np.random.seed(seed) 
    
        # Each string has 5 seeds separated by a space 
        strg_serial   = " ".join(np.random.randint(0,1e8,5).astype(str))
        strg_parallel = " ".join(np.random.randint(0,1e8,5).astype(str))
    
    else: # Fixed seed strings for direct comparison
        strg_serial   = '1 2 3 4 5'
        strg_parallel = '6 7 8 9 10'
        
    return strg_serial,strg_parallel



def f_build_xml(dict_pars,fname):
    
    xml_strg='''<?xml version="1.0"?>
<grid>
  <HMC>
    <StartTrajectory>{start_traj}</StartTrajectory>
    <Trajectories>{total_traj}</Trajectories>
    <MetropolisTest>true</MetropolisTest>
    <NoMetropolisUntil>{therm}</NoMetropolisUntil>
    <StartingType>{start_type}</StartingType>
    <PerformRandomShift>false</PerformRandomShift>
    <MD>
      <name>MinimumNorm2</name>
      <MDsteps>{md_steps}</MDsteps>
      <trajL>{traj_l}</trajL>
    </MD>
  </HMC>
  <Checkpointer>
    <config_prefix>./ckpoint_lat</config_prefix>
    <rng_prefix>./ckpoint_rng</rng_prefix>
    <saveInterval>5</saveInterval>
    <saveSmeared>false</saveSmeared> <!--latest Grid-->
    <smeared_prefix>./ckpoint_lat_smr</smeared_prefix> <!--latest Grid-->
    <format>IEEE64BIG</format>
  </Checkpointer>
  <RandomNumberGenerator>
    <serial_seeds>{seed_serial}</serial_seeds>
    <parallel_seeds>{seed_parallel}</parallel_seeds>
  </RandomNumberGenerator>
  <Action>
    <gauge_beta>{beta}</gauge_beta>
    <Mobius>
        <Ls>{dwf_Ls}</Ls>
        <mass>{mf}</mass>
        <M5>1.8</M5>
        <b>1.5</b>
        <c>0.5</c>
        <StoppingCondition>1e-10</StoppingCondition>
        <MaxCGIterations>30000</MaxCGIterations>
        <ApplySmearing>false</ApplySmearing>
    </Mobius>
  </Action>
</grid>
    '''.format(**dict_pars)

    with open(fname,'w') as f: f.write(xml_strg)

        
def f_build_submit_script(dict_pars,fname,machine):
    '''
    Build submit script for all run types
    '''
    
    app_strg='"$RUN_DIR/build/dweofa_mobius_HSDM_v3 --grid {Lx}.{Lx}.{Lx}.{Lt} --mpi {mpi} --shm 2048 --shm-force-mpi 1 --device-mem 5000 --ParameterFile {ip_xml}"'.format(**dict_pars)
    
    flux=True
    if machine=='tioga':
        if flux:
            submit_strg='''#!/bin/bash
###############
#!/bin/bash
#FLUX: -t 180m
#FLUX: --job-name=HSDM_1
#FLUX: --output=HSDM_1
#FLUX: --error=HSDM_1
#FLUX: -N {N}
#FLUX: -n {nprocs}
#FLUX: --exclusive

echo "--start " `date` `date +%s`
GRID_DIR=../..
source ${{GRID_DIR}}/env.sh
APP="$GRID_DIR/install/gauge_gen_Nc4/bin/dweofa_mobius_HSDM_v3"

echo "GRID_DIR= $GRID_DIR"
echo "RUN_DIR= $RUN_DIR"

# if not used, only one gpu will be used
export MPICH_GPU_SUPPORT_ENABLED=1 

export MPICH_SMP_SINGLE_COPY_MODE=CMA
export MPICH_OFI_NIC_POLICY=GPU

OPTIONS="--decomposition  --comms-concurrent --comms-overlap --debug-mem  --shm 2048 --shm-mpi 1"
PARAMS=" --grid {Lx}.{Lx}.{Lx}.{Lt} --mpi {mpi} --threads 8 --accelerator-threads 8 ${{OPTIONS}} --ParameterFile {ip_xml} "
flux run -N {N} -n {nprocs} -g 1 --verbose --exclusive --setopt=mpibind=verbose:1 $APP $PARAMS


#-------------------------------------------------------------------
# https://github.com/paboyle/Grid/issues/323
# --threads 8: specifies thread count <= OMP_NUM_THREADS
# --accelerator-threads 8: how many threads run on each SM in GPU
#
# options: Grid/util/Init.cc


#-------------------------------------
# Useful links
# Batch System Cross-Reference Guides: https://hpc.llnl.gov/banks-jobs/running-jobs/batch-system-cross-reference-guides
# Batch jobs: https://hpc-tutorials.llnl.gov/flux/section3/
# Flux cheat sheet: https://flux-framework.org/cheat-sheet/

echo "--end " `date` `date +%s`

        '''.format(app=app_strg,**dict_pars)   
    

###older SLURM script    
        else: 
            submit_strg='''#!/bin/bash
################
# Begin LSF Directives
#SBATCH -A latticgc
#SBATCH -t 00:10:00
#SBATCH -J hsdm
#SBATCH -o hsdm.%J
#SBATCH -e hsdm.%J
#SBATCH -N {N}
#SBATCH -n {nprocs}
#SBATCH --exclusive
#SBATCH --gpu-bind=map_gpu:0,1,2,3,7,6,5,4
#SBATCH -c 1
###SBATCH --threads-per-core=1

echo "--start " `date` `date +%s`

echo "GRID_DIR= $GRID_DIR"
echo "RUN_DIR= $RUN_DIR"

export BIND="--cpu-bind=verbose,map_ldom:3,3,1,1,2,2,0,0"

export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=16384
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_SMP_SINGLE_COPY_MODE=CMA
export OMP_NUM_THREADS=8
export MPICH_OFI_NIC_POLICY=GPU
export OPT="--comms-concurrent --comms-overlap "

source $GRID_DIR/setup_env.sh
export TSAN_OPTIONS='ignore_noninstrumented_modules=1'
export LD_LIBRARY_PATH

APP={app}

#srun --gpus-per-task 1 -n64 $BIND $APP > HSDM.out
#srun --gpus-per-task 1 -n64 $APP > HSDM.out
srun -n{nprocs} -o {out_file} $APP

echo "--end " `date` `date +%s`

        '''.format(app=app_strg,**dict_pars)
    
    elif machine=='lassen': 
        submit_strg='''#!/bin/bash
##############
#!/bin/bash
# Begin LSF Directives
#BSUB -P latticgc
#BSUB -W 10
#BSUB -J HSDM.%J
#BSUB -o out_HSDM.%J
#BSUB -e err_HSDM.%J
#BSUB -nnodes {N}
######BSUB --exclusive
####BSUB -c 8
###BSUB --threads-per-core=1

echo "--start " `date` `date +%s`

export BIND="--cpu-bind=verbose,map_ldom:3,3,1,1,2,2,0,0"

export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=16384
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_SMP_SINGLE_COPY_MODE=CMA
export OMP_NUM_THREADS=4
export MPICH_OFI_NIC_POLICY=GPU
export OPT="--comms-concurrent --comms-overlap "


source $GRID_DIR/setup_env.sh
export TSAN_OPTIONS='ignore_noninstrumented_modules=1'
export LD_LIBRARY_PATH

APP={app}
lrun -M -gpu -n{nprocs} -o {out_file} $APP

echo "--end " `date` `date +%s`
    
            '''.format(app=app_strg,**dict_pars)    
    
    with open(fname,'w') as f: f.write(submit_strg)


def f_setup_run_dir(run_type,run_dir,machine,dict_pars):
    '''
    Build run directory and copy files
    '''
    
    assert run_type in ['fresh','checkpoint_start','extend'], "Invalid run_type %s"%(run_type)

    if run_type=='extend':
        assert os.path.exists(run_dir), "Top directory %s doesn't exist"%(run_dir)

        xml_fname=f_get_xml_file_name(run_type,run_dir)
        f_build_xml(dict_pars,xml_fname)
        dict_pars['ip_xml']=xml_fname

        fname=run_dir+'/submit_2_dwf-hsdm.sh'
        f_build_submit_script(dict_pars,fname,machine)
    
    # Can create folders and files for a set of couplings
    elif run_type in ['fresh','checkpoint_start'] : 
        strg='run_Lx-%s_Lt-%s_Ls-%s_beta-%s_mf-%s'%(dict_pars['Lx'],dict_pars['Lt'],dict_pars['dwf_Ls'],\
                                                    dict_pars['beta'],dict_pars['mf'])
        
        fldr=run_dir+'/%s/'%(strg)
        print(fldr)
        
        if os.path.exists(fldr):
            print("Error: Directory %s exists"%(fldr))
            raise SystemError
        else:
            os.makedirs(run_dir+'/{0}'.format(strg))

            fname=fldr+'config.yaml'
            f_write_config(dict_pars,fname)

            xml_fname=f_get_xml_file_name(run_type,fldr)
            f_build_xml(dict_pars,xml_fname)
            dict_pars['ip_xml']=xml_fname
            
            fname=fldr+'submit_1_dwf-hsdm.sh'
            f_build_submit_script(dict_pars,fname,machine)
    
        if run_type=='checkpoint_start':
            print("Copy start config %s"%(dict_pars['ip_conf']))
            shutil.copy(dict_pars['ip_conf'], fldr+'/ckpoint_lat.0')
#             shutil.copy(dict_pars['input_conf_dir']+'/'+'ckpoint_rng.%s'%(dict_pars['config']), fldr+'/ckpoint_rng.0')

 