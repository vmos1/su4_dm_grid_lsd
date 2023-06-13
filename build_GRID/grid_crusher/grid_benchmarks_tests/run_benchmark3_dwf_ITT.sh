#!/bin/bash

#SBATCH -A lgt104_crusher
#SBATCH -t 00:30:00
#SBATCH -J Benchmark_dwf_fp32_1node
#SBATCH -o Benchmark_dwf_fp32_1node.%J
#SBATCH -e Benchmark_dwf_fp32_1node.%J
#SBATCH -N 2
#SBATCH -n 8
#SBATCH -C nvme
#SBATCH --cpus-per-task=7
#SBATCH --ntasks-per-node=8

export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=16384
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_SMP_SINGLE_COPY_MODE=CMA
export OMP_NUM_THREADS=7
export MPICH_OFI_NIC_POLICY=GPU

# New vars
rm -f ./core
ulimit -c unlimited
export OMP_NUM_THREADS=7
export OMP_PROC_BIND=spread
MASK_0="0x00fe000000000000"
MASK_1="0xfe00000000000000"
MASK_2="0x0000000000fe0000"
MASK_3="0x00000000fe000000"
MASK_4="0x00000000000000fe"
MASK_5="0x000000000000fe00"
MASK_6="0x000000fe00000000"
MASK_7="0x0000fe0000000000"
MEMBIND="--mem-bind=map_mem:3,3,1,1,0,0,2,2"
CPU_MASK="--cpu-bind=mask_cpu:${MASK_0},${MASK_1},${MASK_2},${MASK_3},${MASK_4},${MASK_5},${MASK_6},${MASK_7}"

source $GRID_DIR/setup_env.sh
PARAMS=" --accelerator-threads 8 --grid 64.64.32.32 --mpi 2.2.2.2 --comms-sequential --shm 2048 --shm-mpi 1"
srun --gpus-per-task 1 -n16 $BIND ./wrap.sh  $GRID_DIR/install/build-Nc4/benchmarks/Benchmark_ITT $PARAMS ${CPU_MASK} ${MEMBIND} ${APP}

