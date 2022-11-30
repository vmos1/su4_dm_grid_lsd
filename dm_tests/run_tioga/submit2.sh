#!/bin/bash
# Begin LSF Directives
#SBATCH -A lsd
#SBATCH -t 00:10:00
#SBATCH -J hsdm2nodes
#SBATCH -o hsdm2nodes.%J
#SBATCH -e hsdm2nodes.%J
#SBATCH -N 2
#SBATCH -n 8
#SBATCH --exclusive
#SBATCH --gpu-bind=map_gpu:0,1,2,3,7,6,5,4
#SBATCH -c 8
#SBATCH --threads-per-core=1


echo "--start " `date` `date +%s`

export BIND="--cpu-bind=verbose,map_ldom:3,3,1,1,2,2,0,0"

DIR=.
export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=16384
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_SMP_SINGLE_COPY_MODE=CMA
export OMP_NUM_THREADS=4
export MPICH_OFI_NIC_POLICY=GPU
export OPT="--comms-concurrent --comms-overlap "


source $GRID_DIR/setup_env.sh
export TSAN_OPTIONS='ignore_noninstrumented_modules=1'
export LD_LIBRARY_PATH

BETA=10.0
M_F=0.1
N_S=4
PARAMS=" --accelerator-threads 8 --grid 64.64.32.32 --mpi 2.2.2.1 --comms-sequential --shm 2048 --shm-mpi 1"

APP="./$RUN_DIR/dm_tests/build/dweofa_HSDM --grid 16.16.16.16 --mpi 2.2.2.2 --shm 2048 --shm-force-mpi 1 --device-mem 5000 $OPT $BETA $M_F $N_S"

#jsrun --nrs 4 -a4 -g4 -r1 -c40 -dpacked -b packed:10 --latency_priority gpu-cpu --smpiargs=-gpu $APP > SDM.4node
srun --gpus-per-task 1 -n16 $BIND $APP > HSDM.2node

echo "--end " `date` `date +%s`

