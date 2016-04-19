#!/bin/sh
# Note: this script is tailored to Blue Waters
set -eu
mkdir -p ../dist/tmp/hw9
for num_nodes in 8 16 32 64; do
    for m in 001024 016384 102400; do
        for method in 1 2; do
            # for some reason, qsub with stdin is really buggy, so we have to
            # make a temporary file instead
            sed -e "s/{{num_nodes}}/$num_nodes/g;
                    s/{{m}}/$m/g;
                    s/{{method}}/$method/g" <job.sh.template \
                >../dist/tmp/hw9/job.sh
            qsub ../dist/tmp/hw9/job.sh
        done
    done
done
