#!/bin/bash
#SBATCH --partition=rapid
#SBATCH --cpus-per-task=48
#SBATCH --nodes=1
#SBATCH --time=1-00:00:00
#SBATCH --job-name="rap120"
#SBATCH -o out # STDOUT
#SBATCH -e err # STDERR
#SBATCH --export=ALL
#SBATCH --exclusive

#module load hdf5
export OMP_NUM_THREADS=48

folder='../output/'


for i in {0800..1000}; do
     ./RAPTOR model.in $folder/data$i.dat $i
done


#for i in {0900..0910}; do
#    if [$i -lt 10] ; then
#	./RAPTOR model.in $folder/data000$i.dat $i	
#    elif [$i -gt 10 && $i -lt 100] ; then
#	./RAPTOR model.in $folder/data00$i.dat $i
#    elif [$i -gt 100 && $i -lt 1000] ; then
#	./RAPTOR model.in $folder/data0$i.dat $i
#    else
#	./RAPTOR model.in $folder/data$i.dat $i
#    fi
#done
