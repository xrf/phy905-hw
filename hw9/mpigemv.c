#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <cblas.h>
#include <mpi.h>
#include "../utils/utils.h"
#include "../utils/mpi.h"

#define NUM_WARMUPS 1
#define NUM_REPEATS 10
#define TICK_FACTOR 10000
#define ROOT_RANK 0

#ifndef NDEBUG
static void verify_gemv(int is_root,
                        const double *a,
                        const double *x,
                        const double *y,
                        int k,
                        int m)
{
    double *aa, *xx, *yy, *yy0;
    if (is_root) {
        aa = malloc(m * m * sizeof(*aa));
        xx = malloc(m * sizeof(*xx));
        yy = malloc(m * sizeof(*yy));
        yy0 = malloc(m * sizeof(*yy0));
    }
    xtry(MPI_Gather(a, k * m, MPI_DOUBLE,
                    aa, k * m, MPI_DOUBLE,
                    0, MPI_COMM_WORLD));
    xtry(MPI_Gather(x, k, MPI_DOUBLE,
                    xx, k, MPI_DOUBLE,
                    0, MPI_COMM_WORLD));
    xtry(MPI_Gather(y, k, MPI_DOUBLE,
                    yy, k, MPI_DOUBLE,
                    0, MPI_COMM_WORLD));
    if (is_root) {
        cblas_dgemv(CblasRowMajor, CblasNoTrans,
                    m, m, 1., aa, m, xx, 1, 0., yy0, 1);
        for (int i = 0; i < m; ++i) {
            xensure(yy[i] == yy0[i]);
        }
        free(aa);
        free(xx);
        free(yy);
        free(yy0);
    }
}
#endif

enum method {
    allgather = 1,
    circulate = 2
};

int main(int argc, char **argv)
{
    const struct mpi mpi = init_mpi(&argc, &argv);

    /* parse args (unsafe) */
    xensure(argc > 2);
    enum method method = atoi(argv[1]);
    int m = atoi(argv[2]); /* total number of rows/columns */

    double k = m / mpi.size; /* number of rows per process */
    xensure(k * mpi.size == m);

    double *a = malloc(k * m * sizeof(*a));
    double *x = malloc(k * sizeof(*x));
    double *y = malloc(k * sizeof(*y));

    init_random_array_d(a, k * m);
    init_random_array_d(x, k);

    /* initialize benchmark helper */
    parallel_bm parbench;
    bm *bench = init_parallel_bm(&parbench, mpi.rank, ROOT_RANK, NUM_REPEATS);
    set_bm_num_warmups(bench, NUM_WARMUPS);
    set_bm_num_subrepeats(bench, 1);
    if (mpi.rank == ROOT_RANK) {
        set_bm_time_func(bench, &MPI_Wtime);
        set_bm_preferred_time(bench, MPI_Wtick() * TICK_FACTOR);
    }

    switch (method) {

    case allgather: {
        double *xx = malloc(m * sizeof(*xx));
        while (with_bm(bench)) {
            xtry(MPI_Allgather(x, k, MPI_DOUBLE,
                               xx, k, MPI_DOUBLE,
                               MPI_COMM_WORLD));
            cblas_dgemv(CblasRowMajor, CblasNoTrans,
                        k, m, 1., a, m, xx, 1, 0., y, 1);
        }
        free(xx);
        break;
    }

    case circulate:
        /* todo ... */
        break;

    default:
        xensure(0);
    }

#ifndef NDEBUG
    verify_gemv(mpi.rank == 0, a, x, y, k, m);
#endif

    print_bm_stats(bench, "");

    free(a);
    free(x);
    free(y);
    xtry(MPI_Finalize());
}
