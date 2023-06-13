#!/bin/bash
# Begin LSF Directives
#SBATCH -A latticgc
#SBATCH -t 00:10:00
#SBATCH -J Benchmark_dwf_fp32_1node
#SBATCH -o Benchmark_dwf_fp32_1node.%J
#SBATCH -e Benchmark_dwf_fp32_1node.%J
#SBATCH -N 1
#SBATCH -n 8
#SBATCH --exclusive
#SBATCH --gpu-bind=map_gpu:0,1,2,3,7,6,5,4
#SBATCH -c 8
###SBATCH --threads-per-core=1


##export BIND="--cpu-bind=verbose,map_ldom:3,3,1,1,2,2,0,0"

export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=16384
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_SMP_SINGLE_COPY_MODE=CMA
export OMP_NUM_THREADS=8
export MPICH_OFI_NIC_POLICY=GPU

source $GRID_DIR/setup_env.sh
export TSAN_OPTIONS='ignore_noninstrumented_modules=1'
export LD_LIBRARY_PATH

PARAMS=" --grid 64.64.32.32 --mpi 2.2.2.1 --comms-sequential --shm 2048 --shm-mpi 1"
APP="$GRID_DIR/install/build-Nc4/benchmarks/Benchmark_dwf_fp32 $PARAMS"
##srun -n8 $BIND ./wrap $APP > run1_1node.out
srun -n8 $APP > run1_1node.out
echo "--end " `date` `date +%s`
