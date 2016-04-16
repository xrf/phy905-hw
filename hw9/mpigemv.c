#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <cblas.h>
#include <mpi.h>
#include "../utils/utils.h"

#define WARMUP_REPEATS 1
#define NUM_REPEATS 10
#define TICK_FACTOR 10000

struct mpi {
    int rank, size;
};

/** Initialize MPI and return the rank and world size. */
static struct mpi init_mpi(int *argc, char ***argv)
{
    struct mpi r;
    int provided, required = MPI_THREAD_FUNNELED;
    xtry(MPI_Init_thread(argc, argv, required, &provided));
    xensure(provided >= required);
    xtry(MPI_Comm_rank(MPI_COMM_WORLD, &r.rank));
    xtry(MPI_Comm_size(MPI_COMM_WORLD, &r.size));
    return r;
}

static void verify_gemv(int rank,
                        const double *a,
                        const double *x,
                        const double *y,
                        int k,
                        int m)
{
    double *aa, *xx, *yy, *yy0;
    if (rank == 0) {
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
    if (rank == 0) {
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

enum method {
    allgather = 1,
    circulate = 2
};

int main(int argc, char **argv)
{
    double min_time, t;
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

    if (mpi.rank == 0) {
        min_time = MPI_Wtick() * TICK_FACTOR;
        printf("min_time /s = %.17g\n", min_time);
        t = MPI_Wtime();
    }

    switch (method) {

    case allgather:
        for (unsigned i = 0; i < 1; ++i) {
            double *xx = malloc(m * sizeof(*xx));
            xtry(MPI_Allgather(x, k, MPI_DOUBLE,
                               xx, k, MPI_DOUBLE,
                               MPI_COMM_WORLD));
            cblas_dgemv(CblasRowMajor, CblasNoTrans,
                        k, m, 1., a, m, xx, 1, 0., y, 1);
            free(xx);
        }
        break;

    case circulate:
        /* todo ... */
        break;

    default:
        xensure(0);
    }

    /** todo: do both repeats and subrepeats (make a macro?) */
    if (mpi.rank == 0) {
        t = MPI_Wtime() - t;
        printf("time /s = %.17g\n", t);
    }

    verify_gemv(mpi.rank, a, x, y, k, m);

    free(a);
    free(x);
    free(y);
    xtry(MPI_Finalize());
}
