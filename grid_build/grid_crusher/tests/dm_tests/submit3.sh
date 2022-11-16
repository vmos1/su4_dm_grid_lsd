#!/bin/bash
# Begin LSF Directives
#SBATCH -A lgt104_crusher
#SBATCH -t 00:10:00
#SBATCH -J hsdm64nodes
#SBATCH -o hsdm64nodes.%J
#SBATCH -e hsdm64nodes.%J
#SBATCH -N 8 
#SBATCH -n 8
#SBATCH --exclusive
#SBATCH --gpu-bind=map_gpu:0,1,2,3,7,6,5,4
#SBATCH -c 8
#SBATCH --threads-per-core=1


echo "--start " `date` `date +%s`

export BIND="--cpu-bind=verbose,map_ldom:3,3,1,1,2,2,0,0"

DIR=.
#source sourceme.sh   #Assume already sourced in user env
export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=16384
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_SMP_SINGLE_COPY_MODE=CMA
export OMP_NUM_THREADS=4
export MPICH_OFI_NIC_POLICY=GPU
export OPT="--comms-concurrent --comms-overlap "

GRID=/gpfs/alpine/lgt104/proj-shared/ayyar/LSD_projects/build_LSD_grid/install_oct7_2022/
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/sw/crusher/spack-envs/base/opt/cray-sles15-zen3/gcc-11.2.0/hdf5-1.12.1-duogocgjuszctn4kw6he2vgus5kcedxl/lib/:$GRID/install/build-Nc4/Grid/
export LD_LIBRARY_PATH

BETA=10.0
M_F=0.1
N_S=4
PARAMS=" --accelerator-threads 8 --grid 64.64.32.32 --mpi 2.2.2.1 --comms-sequential --shm 2048 --shm-mpi 1"

APP="./../build/dweofa_HSDM --grid 16.16.16.16 --mpi 2.2.2.2 --shm 2048 --shm-force-mpi 1 --device-mem 5000 $OPT $BETA $M_F $N_S"

#jsrun --nrs 4 -a4 -g4 -r1 -c40 -dpacked -b packed:10 --latency_priority gpu-cpu --smpiargs=-gpu $APP > SDM.4node
srun --gpus-per-task 1 -n64 $BIND $APP > HSDM.64node

echo "--end " `date` `date +%s`

