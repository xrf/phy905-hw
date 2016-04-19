# For use on Blue Waters

#PBS -l nodes={{num_nodes}}:ppn={{num_ppn}}:xe
#PBS -l walltime={{walltime}}
#PBS -A babq

export MPICH_NEMESIS_ASYNC_PROGRESS=1
export MPICH_MAX_THREAD_SAFETY=multiple

mpiexec() (
    aprun -N "$PBS_NUM_PPN" "$@"
)
