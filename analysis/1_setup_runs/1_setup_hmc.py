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

    parser = argparse.ArgumentParser(description='Job submission tool usage:\nList of available modes: \n\t- get_families\n\t- new-family\n\t- new-process-definition\n\t- get_configurations', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    add_arg = parser.add_argument

    add_arg('--run_type','-r',type=str,default='fresh',choices=['fresh','extend','checkpoint_start'], required=True, help='Type of run to setup' )
    add_arg('--run_dir','-d',type=str, default='',help='parent directory of run')
    add_arg('--machine','-m',type=str, default='tioga', choices=['cpu','tioga','lassen'],help='Machine on LLNL')
    add_arg('--conf','-c',type=str, default='',help='Full path to checkpoint config for checkpoint start')
    return parser.parse_args()



if __name__=="__main__":
    
    args=parse_args()
#     print(args)
    
    run_type = args.run_type
    run_dir  = args.run_dir 
    conf = args.conf 
    machine = args.machine 
    
    if run_type=='fresh':

        beta_list=[10.6]
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
    