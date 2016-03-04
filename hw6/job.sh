#!/bin/bash
#PBS -j oe -m ae
#PBS -l nodes=1:ppn=16
#PBS -l walltime=10:00
#PBS -l mem=1gb
set -eu
module add GNU/5.2 Python3/3.3.2
cd "$HOME/stuff/phy905-hw/hw6"
make CC=gcc
