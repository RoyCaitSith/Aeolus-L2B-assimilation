#!/bin/bash

#####################################################
# machine set up (users should change this part)
#####################################################

#SBATCH --time=72:00:00
#SBATCH --nodes=3
#SBATCH --ntasks=48
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J 21082318 
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

export SCRATCH_DIRECTORY=/scratch/general/lustre/u1237353/20210824_CON6h_DS1h_Q 
export RUN_WRF_DIRECTORY=$SCRATCH_DIRECTORY/Run_WRF

mpirun -np $SLURM_NTASKS $RUN_WRF_DIRECTORY/wrf.exe >& $RUN_WRF_DIRECTORY/log.wrf

exit 0
