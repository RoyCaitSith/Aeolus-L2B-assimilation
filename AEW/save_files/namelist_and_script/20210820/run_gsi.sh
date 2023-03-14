#!/bin/bash

#SBATCH --time=6:00:00 
#SBATCH --nodes=3
#SBATCH --ntasks=48
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J gsi
#SBATCH -o slurm-%j.out-%N
#SBATCH -e slurm-%j.err-%N
#SBATCH --mail-type=FAIL,BEGIN,END
#SBATCH --mail-user=ROY.FENG@utah.edu

module purge
module load cmake/3.13.3
module load intel/18 impi/18
module load hdf5
module load netcdf-c netcdf-f netcdf-cxx

export PATH="/uufs/chpc.utah.edu/sys/installdir/netcdf/i18/bin:$PATH"
export NETCDF="/uufs/chpc.utah.edu/sys/installdir/netcdf/i18"
export LAPACK_PATH="$MKLROOT"

set -x

RUN_COMMAND="mpirun -genv OMP_NUM_THREADS=1 -np 48 "
${RUN_COMMAND} ./gsi.x > stdout 2>&1
