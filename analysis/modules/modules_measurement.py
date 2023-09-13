
import numpy as np
import matplotlib.pyplot as plt

import subprocess as sp
import sys
import os 
import glob
import pandas as pd
import itertools

import gvar as gv
import h5py


## Modules

#  ## Code to explore hdf5 data
# def get_ds_dictionaries(name, node):
  
#     fullname = node.name
#     if isinstance(node, h5py.Dataset):
#     # node is a dataset
#         print(f'Dataset: {fullname}; adding to dictionary')
#         ds_dict[fullname] = node[:]
#         print('ds_dict size', len(ds_dict)) 
#     else:
#      # node is a group
#         print(f'Group: {fullname}; skipping')  
    
    
# ds_dict= {}    
# with h5py.File(output_dir+f1) as hf:
#     print(hf.visititems(get_ds_dictionaries))
# print(ds_dict)

# ds_dict= {}    
# with h5py.File(output_dir+f2) as hf:
#     print(hf.visititems(get_ds_dictionaries))
# print(ds_dict)


def f_extract_meson(fname,meson_dict):
    '''
    Extract meson info
    '''
    with h5py.File(fname) as hf:
        meson_dict['corr']=np.asarray(hf['meson']['meson_0']['corr'][:].tolist())

    return meson_dict

def f_extract_wi(fname,wi_dict):
    '''
    Extract Ward Identity info
    '''
    with h5py.File(fname) as hf:
        for key1,value1 in hf['wardIdentity'].items():
            wi_dict[key1]=np.array(hf['wardIdentity'][key1][:].tolist())

    return wi_dict
    
    
def f_compute_mresidual(meas_dict):
    '''
    Compute residual mass
    '''
    arr=np.array([i[0]/j[0] for i,j in zip(meas_dict['PJ5q'],meas_dict['meson_corr'])])

    return arr

def f_extract_wilson_flow(fname):
    
    keys=['flow_time','Plaq_density','Clover_density','top_charge','plaq','rect','r_ploop','i_ploop']
    flow_vars=dict.fromkeys(keys)

    with h5py.File(fname) as hf:
        for idx,key in enumerate(keys):
#             print(type(hf['FlowObservables']['FlowObservables_%s'%(idx)]['data']))
            flow_vars[key]=np.array(hf['FlowObservables']['FlowObservables_%s'%(idx)]['data'])
    
    return flow_vars



def f_get_meas(run_dir,epoch,drop_imag=True):
    '''
    Get correlator measurements in a dictionary
    '''
    
    f1='eta_s_2pt.{0}.h5'.format(epoch)
    f2='prop_gauge_DWF.{0}.h5'.format(epoch)

    meson_dict={}
    meson_dict=f_extract_meson(run_dir+f1,meson_dict)

    wi_dict={}
    wi_dict=f_extract_wi(run_dir+f2,wi_dict)
    
    ## Copy each element of wi_dict into meas_dict
    meas_dict=dict(wi_dict)
    
    meas_dict['meson_corr']=meson_dict['corr']
    
    m_res=f_compute_mresidual(meas_dict)
    meas_dict['m_res']=m_res
    
    if drop_imag==True:# Drop imaginary part
        for key in meas_dict.keys():
            if key!='m_res':
                meas_dict[key]=meas_dict[key][:,0]
    
    return meas_dict


def f_plot_mres(meas_dict,plot_ensemble=True,plot_corr=True):
    '''
    Plot residual mass using meas_dict
    '''
    
    ## Plot correlators
#     if imag_part=True: 
#         y1=[i[0] for i in meas_dict['PJ5q']]
#         y2=[i[0] for i in meas_dict['meson_corr']]
    
    
    y1=meas_dict['PJ5q']
    y2=meas_dict['meson_corr']
    x=np.arange(y1.shape[0])

    if plot_corr: 
        plt.figure()
        if plot_ensemble: 
            plt.errorbar(x,gv.mean(y1),gv.sdev(y1),linestyle='',marker='*',label='Axial')
            plt.errorbar(x,gv.mean(y2),gv.sdev(y2),linestyle='',marker='o',label='meson')

        else: 
            plt.plot(x,y1,linestyle='',marker='*',label='Axial')
            plt.plot(x,y2,linestyle='',marker='o',label='meson')

        plt.yscale('log')
        plt.ylabel('correlator')
        plt.legend()
    
    
    ## Plot residual mass
    plt.figure()
    if plot_ensemble: 
        plt.errorbar(x,gv.mean(meas_dict['m_res']),gv.sdev(meas_dict['m_res']),linestyle='',marker='*')
    else: 
        plt.plot(x,meas_dict['m_res'],linestyle='',marker='*')
    plt.ylabel("residual mass")


