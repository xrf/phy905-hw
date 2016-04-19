#!/bin/bash
#PBS -q normal
#PBS -A babq
#PBS -l nodes=16:ppn=16:xe
#PBS -l walltime=30:00
# Note: this script is tailored to Blue Waters
set -eu
export MPICH_NEMESIS_ASYNC_PROGRESS=1
export MPICH_MAX_THREAD_SAFETY=multiple
cd "$PBS_O_WORKDIR"
mkdir -p bench_bandwidth
for size in 512 2048 8192 32768 131072 524288 \
            2097152 8388608 33554432 134217728; do
    np=`expr "$PBS_NUM_NODES" "*" "$PBS_NUM_PPN"`
    half_np=`expr "$np" / 2`
    outfile=bench_bandwidth/${size}.txt
    printf "Benchmarking (%s) ...\n" "$outfile"
    aprun -n "$np" -N "$PBS_NUM_PPN" \
        ../dist/bin/mpibandwidth "$half_np" "$size" |
        # delete the last line of the file because APPARENTLY aprun
        # writes the rusage to standard output (why??)
        sed '$d' >"$outfile".tmp
    mv "$outfile".tmp "$outfile"
done
