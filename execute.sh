#!/bin/sh

#SBATCH -p B4cpu
#SBATCH -N 4
#SBATCH -n 128
#SBATCH -c 4
#SBATCH -t 10:00:00
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-user=naofuji.1220@gmail.com

source /home/issp/materiapps/intel/lammps/lammpsvars.sh

python3 generate.py
srun lammps < make_bubble.input
#python3 gravity.py > gravity.atoms
#srun lammps < gravity.input
