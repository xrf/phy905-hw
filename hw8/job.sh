#!/bin/bash
#PBS -j oe -m ae
#PBS -l nodes=32:ppn=1
#PBS -l walltime=15:00
#PBS -l mem=256mb
set -eu
module add GNU/5.2 Python3/3.3.2
cd "$HOME/stuff/phy905-hw/hw8"
make WSIZE="$PBS_NUM_NODES" bench
