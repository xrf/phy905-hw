#!/bin/bash
#PBS -j oe -m ae
#PBS -l nodes=32:ppn=1
#PBS -l walltime=15:00
#PBS -l mem=256mb
set -eu
module add GNU/4.9 OpenMPI/1.10.0
cd "$HOME/stuff/phy905-hw/hw8"
make CFLAGS="-Wall -Wextra -O3 -std=c11" WSIZE="$PBS_NUM_NODES" bench
