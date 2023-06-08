#!/bin/bash
# Begin LSF Directives
#SBATCH -A latticgc
#SBATCH -t 00:10:00
#SBATCH -J Benchmark_ITT
#SBATCH -o Benchmark_ITT.%J
#SBATCH -e Benchmark_ITT.%J
#SBATCH -N 2
#SBATCH -n 8
#SBATCH --exclusive
#SBATCH --gpu-bind=map_gpu:0,1,2,3,7,6,5,4
#SBATCH -c 8
###SBATCH --threads-per-core=1
###export BIND="--cpu-bind=verbose,map_ldom:3,3,1,1,2,2,0,0"

export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=16384
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_SMP_SINGLE_COPY_MODE=CMA
export OMP_NUM_THREADS=8
export MPICH_OFI_NIC_POLICY=GPU

source $GRID_DIR/setup_env.sh
export TSAN_OPTIONS='ignore_noninstrumented_modules=1'
export LD_LIBRARY_PATH

## PARAMS=" --accelerator-threads 8 --grid 64.64.32.32 --mpi 2.2.2.2 --comms-sequential --shm 2048 --shm-mpi 1"
PARAMS=" --grid 64.64.32.32 --mpi 2.2.2.2 --comms-concurrent --comms-overlap --shm 2048 --shm-mpi 1"
APP="$GRID_DIR/install/build-Nc4/benchmarks/Benchmark_ITT $PARAMS"
echo $APP
##srun --gpus-per-task 1 -n16 $BIND ./wrap.sh  $GRID_DIR/install/build-Nc4/benchmarks/Benchmark_ITT $PARAMS
##srun -n16 $BIND ./wrap $APP > run3_2node.out
srun -n16 $APP > run3_2node.out
echo "--end " `date` `date +%s`
