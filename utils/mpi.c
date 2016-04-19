#include <mpi.h>
#include "utils.h"
#include "mpi.h"

struct mpi init_mpi(int *argc, char ***argv)
{
    struct mpi r;
    int provided, required = MPI_THREAD_FUNNELED;
    xtry(MPI_Init_thread(argc, argv, required, &provided));
    xensure(provided >= required);
    xtry(MPI_Comm_rank(MPI_COMM_WORLD, &r.rank));
    xtry(MPI_Comm_size(MPI_COMM_WORLD, &r.size));
    return r;
}

static void broadcast_i(void *root, int *x)
{
    xtry(MPI_Bcast(x, 1, MPI_INT, *(int *)root, MPI_COMM_WORLD));
}

bm *init_parallel_bm(parallel_bm *self, int rank, int root)
{
    bm *bench = parallel_bm_as_bm(self);
    self->_root = root;
    *bench = make_bm();
    set_bm_broadcast_func(bench, &broadcast_i, &self->_root);
    if (rank != root) {
        set_bm_time_func(bench, NULL);
    }
    return bench;
}

bm *parallel_bm_as_bm(parallel_bm *self)
{
    return &self->_bench;
}
