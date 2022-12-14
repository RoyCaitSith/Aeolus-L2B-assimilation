#!/bin/bash

#####################################################
# machine set up (users should change this part)
#####################################################

#SBATCH --time=72:00:00
#SBATCH --nodes=4
#SBATCH --ntasks=96
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J 21082418 
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

module purge
module load intel-oneapi-compilers/2021.4.0
module load openmpi/4.1.1
module load netcdf-c/4.8.1 netcdf-fortran/4.5.3
module load hdf5
module load perl

export NETCDF="/uufs/chpc.utah.edu/sys/spack/linux-rocky8-nehalem/intel-2021.4.0/netcdf"

export SCRATCH_DIRECTORY=/scratch/general/lustre/u1237353/CON6h_Aeolus6h_082418_Hybrid_C01 
export RUN_WRF_DIRECTORY=$SCRATCH_DIRECTORY/Run_WRF

mpirun -np $SLURM_NTASKS $RUN_WRF_DIRECTORY/wrf.exe >& $RUN_WRF_DIRECTORY/log.wrf

exit 0
