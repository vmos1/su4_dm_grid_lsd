#!/bin/bash
# #SBATCH -p debug

#SBATCH -N 1
#SBATCH -n 8
#SBATCH --exclusive
#SBATCH --gpu-bind=map_gpu:0,1,2,3,7,6,5,4
#SBATCH -c 8

Lattice="16.16.16.8"
MPIGrid="2.2.2.1"

machine=tioga
mkdir ${machine}-${SLURM_JOB_ID}

cd $SLURM_SUBMIT_DIR
exec > ${SLURM_SUBMIT_DIR}/${machine}-${SLURM_JOB_ID}/${SLURM_JOB_NAME}-${SLURM_JOB_ID}.${machine}.out 2>&1


echo "--------------------------------"
echo "SLURM job running on: `hostname`"
echo "in directory:         `pwd`"
echo "SLURM jobid:          ${SLURM_JOB_ID}"
echo "SLURM #nodes:         ${SLURM_NNODES}"
echo "SLURM tasks per node: ${SLURM_TASKS_PER_NODE}"
echo "SLURM #ntasks:        ${SLURM_NTASKS}" 
echo "Nodefile: ${SLURM_JOB_NODELIST}"
echo "--------------------------------"
lscpu

echo "# time-start "`date`
TotalTic=`date +%s`

export BIND="--cpu-bind=verbose,map_ldom:3,3,1,1,2,2,0,0"

export MPIR_CVAR_GPU_EAGER_DEVICE_MEM=16384
export MPICH_GPU_SUPPORT_ENABLED=1
export MPICH_SMP_SINGLE_COPY_MODE=CMA
export OMP_NUM_THREADS=8
export MPICH_OFI_NIC_POLICY=GPU

source $GRID_DIR/setup_env.sh
module list

cat << EOF > ${machine}-${SLURM_JOB_ID}/select_gpu
#!/bin/bash

export ROCR_VISIBLE_DEVICES=\$SLURM_LOCALID
exec \$*
EOF
chmod +x ./${machine}-${SLURM_JOB_ID}/select_gpu

input=DWFtest
sed -e "s/MACHINE_JOBID_/${machine}-${SLURM_JOB_ID}/" < $input.xml > ${machine}-${SLURM_JOB_ID}/${input}.xml

#BINARY=/usr/workspace/lsd/witzel2/GRID-develop-2023-06-03/install-tioga/bin/HadronsXmlRun
BINARY=$GRID_DIR/grid_prefix/bin/HadronsXmlRun
PARAMS=" --accelerator-threads 8 --grid ${Lattice} --mpi ${MPIGrid} --comms-sequential --shm 2048 --shm-mpi 1"

echo "srun --gpus-per-task 1 -n8 $BIND ./${machine}-${SLURM_JOB_ID}/select_gpu $BINARY ${machine}-${SLURM_JOB_ID}/${input}.xml $PARAMS"
srun --gpus-per-task 1 -n8 $BIND ./${machine}-${SLURM_JOB_ID}/select_gpu $BINARY ${machine}-${SLURM_JOB_ID}/${input}.xml  $PARAMS

############################################################################################# 
############################################################################################# 

TotalToc=`date +%s`
echo "# time-finish "`date`

TotalTime=$(( $TotalToc - $TotalTic ))
TotalHours=`echo "$TotalTime / 3600" | bc -l`
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "Total time  $TotalTime [sec] = $TotalHours [h]"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
