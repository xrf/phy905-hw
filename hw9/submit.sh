#!/bin/sh
set -eu
for num_nodes in 8 16 32 64; do
    for m in 001024 016384 102400; do
        for method in 1 2; do
            NAME=job.sh \
                ../utils/submit \
                "num_nodes=$num_nodes" \
                "num_ppn=16" \
                "walltime=15:00" \
                "mem=16gb" \
                "m=$m" \
                "method=$method" \
                "$@"
        done
    done
done
