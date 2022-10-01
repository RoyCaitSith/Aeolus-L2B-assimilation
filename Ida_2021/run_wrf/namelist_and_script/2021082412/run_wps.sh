#!/bin/bash

#####################################################
# machine set up (users should change this part)
#####################################################

#SBATCH --time=72:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --account=zpu-kp
#SBATCH --partition=zpu-kp
#SBATCH -J 21082412 
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

export WORK_DIRECTORY=/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng
export SCRATCH_DIRECTORY=/scratch/general/lustre/u1237353/CON6h_082418_Hybrid_C07 
export RUN_WRF_DIRECTORY=$SCRATCH_DIRECTORY/Run_WRF

ln -sf $WORK_DIRECTORY/WPS/geogrid.exe $RUN_WRF_DIRECTORY/geogrid.exe
ln -sf $WORK_DIRECTORY/WPS/ungrib/Variable_Tables/Vtable.GFS $RUN_WRF_DIRECTORY/Vtable
ln -sf $WORK_DIRECTORY/WPS/ungrib.exe $RUN_WRF_DIRECTORY/ungrib.exe
ln -sf $WORK_DIRECTORY/WPS/link_grib.csh $RUN_WRF_DIRECTORY/link_grib.csh
ln -sf $WORK_DIRECTORY/WPS/metgrid.exe $RUN_WRF_DIRECTORY/metgrid.exe
$RUN_WRF_DIRECTORY/link_grib.csh $SCRATCH_DIRECTORY/GFS_Boundary_Condition_Data/gfs* $RUN_WRF_DIRECTORY
mv $SCRATCH_DIRECTORY/namelist.wps $RUN_WRF_DIRECTORY/namelist.wps

$RUN_WRF_DIRECTORY/geogrid.exe >& $RUN_WRF_DIRECTORY/log.geogrid
$RUN_WRF_DIRECTORY/ungrib.exe >& $RUN_WRF_DIRECTORY/log.ungrib 
$RUN_WRF_DIRECTORY/metgrid.exe >& $RUN_WRF_DIRECTORY/log.metgrid

ln -sf $SCRATCH_DIRECTORY/Metgrid_Data/met_em* $RUN_WRF_DIRECTORY
ln -sf $WORK_DIRECTORY/WRF/run/* $RUN_WRF_DIRECTORY
mv $SCRATCH_DIRECTORY/namelist.input $RUN_WRF_DIRECTORY/namelist.input

mpirun -np $SLURM_NTASKS $RUN_WRF_DIRECTORY/real.exe >& $RUN_WRF_DIRECTORY/log.real 

exit 0
