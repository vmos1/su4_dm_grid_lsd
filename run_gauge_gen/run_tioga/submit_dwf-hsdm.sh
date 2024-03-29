#!/bin/bash
# Begin LSF Directives
#SBATCH -A latticgc
#SBATCH -t 00:10:00
#SBATCH -J hsdm 
#SBATCH -o hsdm.%J
#SBATCH -e hsdm.%J
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --exclusive
#SBATCH --gpu-bind=map_gpu:0,1,2,3,7,6,5,4
#SBATCH -c 8
#####SBATCH --threads-per-core=1


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

APP="$RUN_DIR/build/dweofa_mobius_HSDM_v2 --grid 16.16.16.8 --mpi 2.2.2.1 --shm 2048 --shm-force-mpi 1 --device-mem 5000 --ParameterFile ip_hmc_mobius.xml"
srun -n8 $APP > HSDM.8rank.out

echo "--end " `date` `date +%s`

