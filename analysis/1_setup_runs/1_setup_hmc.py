import numpy as np
import os
import argparse
import subprocess as sp
import shutil
import glob

import yaml
from datetime import datetime

from utils import *

def parse_args():
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(description='Job setup tool', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    add_arg = parser.add_argument

    add_arg('--run_type','-r',type=str,default='fresh',choices=['fresh','extend','checkpoint_start'], required=True, help='Type of run to setup' )
    add_arg('--run_dir','-d',type=str, default='',help='parent directory of run')
    add_arg('--machine','-m',type=str, default='tioga', choices=['cpu','tioga','lassen'],help='Machine on LLNL')
    add_arg('--conf','-c',type=str, default='',help='Full path to checkpoint config for checkpoint start')
    return parser.parse_args()



def f_setup_dict_pars(run_type,run_dir,dict_pars):
    '''
    Return dictionary dict_pars with details of run
    Doesn't not modify any files
    '''
    
    assert run_type in ['fresh','checkpoint_start','extend'], "Invalid run_type %s"%(run_type)
    
    
    if run_type=='fresh': ## Fresh run with parameters specified below. Pick start_type 

        Lx=16
        Lt=8
        N=1
        mx,my,mz,mt=2,2,2,1
        Ls=16
        
        dict_pars.update({
            'Lx':Lx, 'Lt':Lt, # Lattice size 
            'F_action': 'Mobius_dwf',

            'traj_l':2, 'md_steps':15, 
        #     'beta':beta, 'mf':mf, 
            'dwf_Ls':Ls, 
            'mpi':".".join([str(i) for i in [mx,my,mz,mt]]),
            'nprocs': mx*my*mz*mt,
            'N':N,  ## Number of nodes
            'total_traj': 700,
            'start_type': 'ColdStart',   # Valid [HotStart, ColdStart, TepidStart, CheckpointStart]
            'start_traj': 0,
            'therm': 10,
            'out_file': 'HSDM1.out'
                  })

    elif run_type=='checkpoint_start': # Start new run with a starting config file

        config_file=dict_pars['ip_conf']
        assert os.path.isfile(config_file) ,"File %s doesn't exist"%(config_file)

        Lx=24; Lt=12
        N=1
        mx,my,mz,mt=2,2,2,1
        Ls=16
        beta=14.0
        mf=0.1
        dict_pars.update({
            'Lx':Lx, 'Lt':Lt, # Lattice size 
            'F_action': 'Mobius_dwf',

            'traj_l':2, 'md_steps':15, 
            'beta':beta, 'mf':mf, 
            'dwf_Ls':Ls, 
            'mpi':".".join([str(i) for i in [mx,my,mz,mt]]),
            'nprocs': mx*my*mz*mt,
            'N':N, 
            'total_traj': 200,
            'start_type': 'CheckpointStart',
            'start_traj': 0,
            'start_config': config_file,
            'therm':0, ## Thermalization ( non-zero for fresh run )
            'out_file': 'HSDM1.out'
                  })

    elif run_type=="extend": # Extend run with same paramters with last saved configuration

        last=f_get_last_checkpoint(run_dir)
        print(last)
        config_file=run_dir+'ckpoint_lat.%s'%(last)
        print("Last checkpoint",last)

        input_dict=f_read_config(run_dir+'/config.yaml')

        dict_pars={}
        for key in input_dict.keys():
            dict_pars[key]=input_dict[key]

        dict_pars.update({
            'start_type': 'CheckpointStart',   # Valid [HotStart, ColdStart, TepidStart, CheckpointStart]
            'start_traj': last,
            'out_file': f_get_out_filename(run_dir),
            'total_traj': 700,
            'therm': 0,
            'starg_config': config_file,
                  })
    
    dict_pars['seed_serial'],dict_pars['seed_parallel'] = f_create_seed_string(mode='timestamp')

    
    return dict_pars


if __name__=="__main__":
    
    args=parse_args()
#     print(args)
    
    run_type = args.run_type
    run_dir  = args.run_dir 
    conf = args.conf 
    machine = args.machine 
    
    if run_type=='fresh':

        beta_list=[10.6,10.8,10.9]
        m_list=[0.1]
        for beta in beta_list:
            for mf in m_list:
                dict_pars={}
                dict_pars['beta'] = beta
                dict_pars['mf']   = mf
                
                dict_pars=f_setup_dict_pars(run_type,run_dir,dict_pars)
                f_setup_run_dir(run_type,run_dir,machine,dict_pars)

    elif run_type=='checkpoint_start':
        dict_pars={'ip_conf':conf}

        dict_pars=f_setup_dict_pars(run_type,run_dir,dict_pars)
        f_setup_run_dir(run_type,run_dir,machine,dict_pars)
        
    else: 
        dict_pars={}

        dict_pars=f_setup_dict_pars(run_type,run_dir,dict_pars)
        f_setup_run_dir(run_type,run_dir,machine,dict_pars)

    print(dict_pars)
    