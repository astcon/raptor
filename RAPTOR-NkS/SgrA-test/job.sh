#!/bin/bash
#SBATCH --partition=fat
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:0
#SBATCH --time=7-00:00:00
#SBATCH --job-name=HR
#SBATCH --mail-type=ALL
#SBATCH -o out # STDOUT
#SBATCH -e err # STDERR

#


export OMP_PROC_BIND=spread
export OMP_PLACES=threads




export OMP_NUM_THREADS=48

folder='../NKM1-REF3DHR/output'

for i in {0100..0300}; do
     ./RAPTOR model.in $folder/data$i.dat $i
done     
#./RAPTOR model.in $folder/data0699.dat 699

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
