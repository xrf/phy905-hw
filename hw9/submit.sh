#!/bin/sh
# Note: this script is tailored to Blue Waters
set -eu
for num_nodes in 8 16 32 64; do
    sed "s/{{num_nodes}}/$num_nodes/g" job.sh.template | qsub
done
