#!/bin/bash
{{prelude}}
set -eu
cd "${PBS_O_WORKDIR-.}"
np=`expr "${PBS_NUM_NODES-1}" "*" "${PBS_NUM_PPN-1}"`
mkdir -p bench
m={{m}}
method={{method}}
outfile=bench/${np}_${method}_${m}.txt
echo "Benchmarking ($outfile) ..."
mpiexec -n "$np" ../dist/bin/mpigemv "$outfile".tmp "$method" "$m"
mv "$outfile".tmp "$outfile"
