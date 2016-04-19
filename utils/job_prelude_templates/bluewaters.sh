# For use on Blue Waters

#PBS -l nodes={{num_nodes}}:ppn={{num_ppn}}:xe
#PBS -l walltime={{walltime}}
#PBS -A babq

export MPICH_NEMESIS_ASYNC_PROGRESS=1
export MPICH_MAX_THREAD_SAFETY=multiple

mpiexec() (
    np=1
    while [ $# -gt 0 ]; do
        case $1 in
            --)
                shift
                break;;
            -np)
                shift
                if [ $# -le 0 ]; then
                    echo >&2 "error: expected argument after -np"
                    return 1
                fi
                np=$1
                shift;;
            -*)
                echo >&2 "error: unknown argument: $1"
                return 1;;
            *)
                break;;
        esac
    done
    aprun -n "$np" -N "$PBS_NUM_PPN" "$@"
)
