#!/bin/bash
{{prelude}}
set -eu
cd "${PBS_O_WORKDIR-.}"
np=`expr "${PBS_NUM_NODES-1}" "*" "${PBS_NUM_PPN-1}"`
mkdir -p bench_bandwidth
half_np=`expr "$np" / 2`
for size in 512 2048 8192 32768 131072 524288 \
            2097152 8388608 33554432; do
    outfile=bench_bandwidth/${size}.txt
    echo "Benchmarking ($outfile) ..."
    mpiexec -n "$np" ../dist/bin/mpibandwidth "$outfile".tmp "$half_np" "$size"
    mv "$outfile".tmp "$outfile"
done
