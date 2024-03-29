#!/bin/bash
# Begin LSF Directives
#SBATCH -A latticgc
#SBATCH -t 00:10:00
#SBATCH -J sdm4nodes
#SBATCH -o sdm4nodes.%J
#SBATCH -e sdm4nodes.%J
#SBATCH -N 4
#SBATCH -n 8
#SBATCH --exclusive
#SBATCH --gpu-bind=map_gpu:0,1,2,3,7,6,5,4
#SBATCH -c 8
#SBATCH --threads-per-core=1


echo "--start " `date` `date +%s`

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

traj_l=1
md_steps=30
BETA=11.0
M_F=-0.6443 # kappa=0.1490

APP="$RUN_DIR/build/hmc_SDM --grid 16.16.16.32 --mpi 2.2.2.4 --shm 2048 --shm-force-mpi 1 --device-mem 5000 --Trajectories 100 --Thermalizations 10 $OPT $traj_l $md_steps $BETA $M_F"
## srun --gpus-per-task 1 -n32 $BIND $APP > SDM.4node
srun --gpus-per-task 1 -n32 $APP > SDM.4node

echo "--end " `date` `date +%s`

