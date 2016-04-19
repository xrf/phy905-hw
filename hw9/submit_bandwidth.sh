#!/bin/sh
set -eu
NAME=job_bandwidth \
    ../utils/submit \
    "num_nodes=4" \
    "num_ppn=1" \
    "walltime=30:00" \
    "mem=1gb" \
    "$@"
