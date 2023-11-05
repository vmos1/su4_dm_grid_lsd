import numpy as np
import pandas as pd
import gvar as gv
import yaml
import subprocess as sp



def f_write_config(input_dict,fname):
    
    with open(fname,'w') as f:
        yaml.dump(input_dict,f,sort_keys=False)
    
def f_read_config(fname):
    
    with open(fname,'r') as f:
        config_dict=yaml.load(f, Loader=yaml.SafeLoader)
        
    return config_dict


def f_get_plaquette(fname,dict1):
    '''
    Get Plaquette from Grid output file
    '''
    try: 
        cmd="grep 'Plaquette' %s"%(fname)
        op=sp.check_output(cmd,shell=True).decode().split('\n') # decode bytes to string and split by newlines
        op=[i for i in op if i] # Drop null string        

        arr=np.array([[int(i.split('[ ')[-1].split(' ]')[0]), np.float64(i.split(' ')[-1])] 
                         for i in op])
        
        ## Hack for when Plaquette is printed twice : smeared and unsmeared
        arr=arr[0::2]
        
        dict1['Plaquette']=arr[:,1]
        dict1['iter'] = arr[:,0]
        
    except Exception as e: 
        print("Couldn't extract Plaquette values")
        print(e)
    
    return dict1


def f_get_polyakov(fname,dict1):
    '''
    Get Polyakov loop as complex number from Grid output file
    '''
    try: 
        cmd="grep 'Polyakov' %s"%(fname)
        op=sp.check_output(cmd,shell=True).decode().split('\n') # decode bytes to string and split by newlines
        op=[i for i in op if i] # Drop null string

        arr=[]
        for i in op: 
            strg=i.split(' ')[-1][1:-1]
            arr.append(complex(np.float64(strg.split(',')[0]),np.float64(strg.split(',')[1])))
    
        dict1['Polyakov']=arr

    except Exception as e: 
        print("Couldn't extract Polyakov values")
        print(e)
    
    return dict1


def f_get_traj_time(fname,dict1):
    '''
    Get Trajectory time from Grid output file
    '''
    
    try: 
        cmd="grep 'Total time for trajectory' %s"%(fname)
        op=sp.check_output(cmd,shell=True).decode().split('\n') # decode bytes to string and split by newlines
        op=[i for i in op if i] # Drop null string
        
        arr=[np.float32(i.split(': ')[-1]) for i in op]
        dict1['Traj_time']=arr

    except Exception as e: 
        print("Couldn't extract total Traj times")
        print(e)
        
    return dict1



def f_get_metropolis(fname,dict1,lgth):
    '''
    Get Metropolis info from Grid output file
    '''
    
    try: 
        cmd="grep 'Metropolis_test' %s"%(fname)
        op=sp.check_output(cmd,shell=True).decode().split('\n') # decode bytes to string and split by newlines
        op=[i for i in op if i] # Drop null string

        ## Other arrays have equilibriation data, metropolis doesn't. So we need to add nans to make them the same size
        arr_temp=[1 if (i.split(' ')[-1]=='ACCEPTED') else 0 for i in op] # Accept =1 , Reject = 0
        skip=lgth-len(arr_temp)
        arr_skip=[np.nan for i in range(skip)]
        arr=np.array(arr_skip+arr_temp)
        dict1['Accept']=arr

    except Exception as e: 
        print("Couldn't extract total Metropolis info")
        print(e)
    
    return dict1

def f_parse_grid_data(fname):
    '''
    Combine data (Plaquette, Polyakov loop, Trajectory time, Metropolis info) 
    from output file for a single run into dataframe
    '''
    dict1={}
    
    f_get_plaquette(fname,dict1)
    
    f_get_polyakov(fname,dict1)
    
    f_get_traj_time(fname,dict1)    
    
    ## Check if list sizes are unequal
    size_lst=[len(val) for val in dict1.values()]
    lg=size_lst[0]
    for i in size_lst:
        if i!=lg: 
            print("Unequal sizes of dict elements")
            print([(key,len(val)) for key,val in dict1.items()])
    
    lgth = min([len(i) for i in dict1.values()])
    f_get_metropolis(fname,dict1,lgth)

    ## Store in DataFrame
    df=pd.DataFrame([])
    for key in dict1.keys():
        df[key]=pd.Series(dict1[key])
        
    return df


def f_jackknife(arr):
    '''Jackknife an input array to get sdev '''
    
    N=arr.shape[0]
    arr_samples=np.zeros(N) # Array to store samples
    
    for i in range(N):
        arr2=np.delete(arr,i)
        arr_samples[i]=np.mean(arr2)
    
    # Compute mean and std. deviation
    mean=np.mean(arr_samples)
    err=np.sqrt( np.sum((arr_samples-mean)**2) * ((N-1)/N) ) # sqrt( (N-1) * variance ) for jackknife

    return gv.gvar(mean,err)


def f_moments(y,L):
    ''' Compute susceptibility and Kurtosis for observables'''
    
    
    mode=2
    
    if mode==1: ## Using gvar for error propagation
        print("Using Mode 1: gvars for computing moments")
        m=[gv.gvar(0,0) for i in range(5)]  # List to store moments
        m[0]=gv.gvar(1,1e-16) # zeroth moment is 1
        for i in range(1,5):
            m[i]=gv.dataset.avg_data(y**i)

        # Check moments obtained by gvar, with direct calculation
#         n=[gv.gvar(0,0) for i in range(5)]  # List to store moments
#         n[0]=gv.gvar(1,1e-16) # zeroth moment is 1
#         for i in range(1,5):
#             arr=y**i
#             n[i]=gv.gvar(np.mean(arr),np.std(arr)/np.sqrt(arr.shape[0]))

        sus=(L**3)*(m[2]-(m[1]**2))
        if sus>1e-7: 
            kurt=(m[4] - 4* m[3] *m[1] + 6* m[2]* (m[1]**2) - 3* (m[1]**4))/(sus**2)
        else: kurt=gv.gvar(np.nan,np.nan)
    
    elif mode==2: ## Propagating errors for highly correlated variables doesn't work, so we use jackknife
        ### Compute arrays of moments
        m=[y**i for i in range(0,5)] # List to store powers of input

        ## Compute sus and kurt by jackknifing elements of this list
        arr=(y - np.mean(y))**2
        sus=(L**3) * f_jackknife(arr)
        
        if sus>1e-7:
    #         arr=(m[4] - 4* m[3] *m[1] + 6* m[2]* (m[1]**2) - 3* (m[1]**4))/(sus**2)
            arr=((y - np.mean(y))**4)
            kurt= f_jackknife(arr) / (gv.mean(sus)**2)
        else: kurt=gv.gvar(np.nan,np.nan)
    
    return sus,kurt

def f_autocorr(a1):
    ''' 
    Compute the autocorrelation function of a given 1D array
    '''
    
    lgth=len(a1)
    
    auto_corr=np.ones(lgth-1,dtype=np.float64)
    
    avg=np.average(a1)
    var=np.var(a1)
    
    # Deviation from the mean
    a2=a1-avg

    mode=2
    
    if mode==1: # Simple method, slower
        for t in range(0,lgth-1):
            auto_corr[t] = (np.mean([(a2[i]*a2[i+t]) for i in range(lgth-t)]))/(var)
        
    elif mode==2: # Faster method with numpy array        
#         auto_corr=np.array([1. if l==0 else np.sum(a2[l:]*a2[:-l])/(lgth*var) for l in range(0,lgth-1)])
        auto_corr=np.array([1. if l==0 else np.mean(a2[l:]*a2[:-l])/(var) for l in range(0,lgth-1)])

    return auto_corr


def f_autocorr_time(a1):
    '''
    Compute autocorrelation array and then compute autocorrelation time as epoch to attain (1/e) th value
    '''
    
    # Compute autocorr array
    auto_corr=f_autocorr(a1)
    
    ## Autocorrelation time as 1/e of 0th value
    for count,i in enumerate(auto_corr):
        if i < (1.0/np.e):
#             print("Autocorr",count,i)
            return count

    print("Error: Autocorr doesn't drop to 1/e")
    return np.inf


def f_get_summary_data(df,L,dict1,equil=50):
    '''
    Get data averaged over Monte-Carlo time for a single run
    '''
    
    drop_idx = equil
    
    if df.shape[0]<=equil:
        return dict1
    
    ## Plaquette 
    y=df.Plaquette.values[drop_idx:]
    dict1['plaq'] = gv.dataset.avg_data(y)
    
    # Susceptibility and Binder cumulant
    dict1['sus_plaq'],dict1['kurt_plaq']=f_moments(y,L)
    
    # Autocorrelation time 
    dict1['plaq_autocorr'] = f_autocorr_time(y)
    
    ## Polyakov Loop
    y=np.abs(df.Polyakov.values[drop_idx:])
    dict1['polyakov']=gv.dataset.avg_data(y)
    
    # Susceptibility and Binder cumulant
    dict1['sus_poly'],dict1['kurt_poly']=f_moments(y,L)

    # Autocorrelation time 
    dict1['poly_autocorr'] = f_autocorr_time(y)
#     print(f_autocorr(y))
    
    ## Trajectory time
    y=df.Traj_time.values[drop_idx:]
    dict1['traj_time']=gv.dataset.avg_data(y)
    
    
    ## Acceptance info
    y=df['Accept'].dropna().values
    Act=y[y==1].shape[0]
    Rjt=y[y==0].shape[0]
    accpt=Act* 100 /(Act+Rjt)

    dict1['accept']=accpt

    ## num of configs
    y=df.Plaquette.values[drop_idx:]
    dict1['num_conf']=y.shape[0]
    
    return dict1

def f_merge_df_successive_runs(df,df_a):
    '''
    HMC runs are usually extended, resulting in multiple output files
    This code merges the dataframe from the output files, in order of trajectory
    '''
    
    # Lowest iteration of second run
    start_run2=int(np.min(df_a.iter.values))
    end_run1=int(np.max(df.iter.values))
    assert (start_run2-end_run1)<=1, "Gap between two runs. Run 1 ends %s , next run starts %s" %(end_run1,start_run2)
    
    # Drop last few iterations that are repeated in next run
    df=df[df.iter<start_run2]
    df=pd.concat([df,df_a],ignore_index=True)
    
    return df


if __name__=="__main":
    
    # Test jackknife
    arr=np.random.normal(5,1,10)
    f_jackknife(arr)
    
    