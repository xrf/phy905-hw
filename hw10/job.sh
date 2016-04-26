#!/bin/bash
#PBS -l nodes=64:ppn=16:xe
#PBS -l walltime=65:00
#PBS -A babq
set -eu
cd "${PBS_O_WORKDIR-.}"

cleanup() {
    rm -fr "$SCRATCH"/*.out
}

. ../dist/tmp/ioda-vars.sh

mkdir -p "$SCRATCH"
cleanup
aprun -n 1024 -ppn 16 -maxtime 20:00 ../dist/bin/ioda 16384 16384 32
lfs getstripe "$SCRATCH"/*.out
cleanup
aprun -n 1024 -ppn 16 -maxtime 20:00 ../dist/bin/ioda 16384 16384 16
lfs getstripe "$SCRATCH"/*.out
cleanup
aprun -n 1024 -ppn 16 -maxtime 20:00 ../dist/bin/ioda 16384 16384 0
lfs getstripe "$SCRATCH"/*.out
cleanup
