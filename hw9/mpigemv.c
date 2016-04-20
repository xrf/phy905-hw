#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cblas.h>
#include <mpi.h>
#include "../utils/utils.h"
#include "../utils/mpi.h"

#define NUM_WARMUPS 1
#define NUM_REPEATS 10
#define TICK_FACTOR 10000
#define ROOT_RANK 0
#define EPSILON 1e-12

static void clear_array_d(double *x, size_t count)
{
    /* we do not use memset explicitly here because the C/C++ standard does
       not mandate 0.0 as having a bitwise-zero representation; instead, we
       let the compiler optimize this into memset when applicable */
    double *const x_end = x + count;
    for (; x != x_end; ++x) {
        *x = 0.;
    }
}

static void swap_dp(double **px, double **py)
{
    double *p = *px;
    *px = *py;
    *py = p;
}

#ifndef NDEBUG
static void verify_gemv(int is_root,
                        const double *a,
                        const double *x,
                        const double *y,
                        int k,
                        int m)
{
    double *aa = NULL, *xx = NULL, *yy = NULL, *yy0 = NULL;
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
            if (!(fabs(yy[i] - yy0[i]) <= EPSILON)) {
                fprintf(stderr,
                        "***error: yy[%i] expected to be %f but got %f\n",
                        i,
                        yy0[i],
                        yy[i]);
                fflush(stderr);
                abort();
            }
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
    /* srand(0) has the same effect as srand(1) on most implementations;
       offset it by one to avoid this */
    srand(mpi.rank + 1);

    /* parse args (unsafe) */
    xensure(argc == 4);
    const char *outfile = argv[1];      /* output filename */
    enum method method = atoi(argv[2]);
    int m = atoi(argv[3]);              /* total number of rows/columns */

    /* redirect stdout to a file because apparently Cray's MPI runner (aprun)
       thought it'd be a good idea to dump diagnostic messages to stdout */
    xtry(!freopen(outfile, "w", stdout));

    int k = m / mpi.size; /* number of rows per process */
    xensure(k * mpi.size == m);

    double *a = malloc(k * m * sizeof(*a));
    double *x = malloc(k * sizeof(*x));
    double *y = malloc(k * sizeof(*y));

    init_random_array_d(a, k * m);
    init_random_array_d(x, k);

    /* initialize benchmark helper */
    parallel_bm parbench;
    bm *bench = init_parallel_bm(&parbench, mpi.rank, ROOT_RANK);
    set_bm_num_repeats(bench, NUM_REPEATS);
    set_bm_num_warmups(bench, NUM_WARMUPS);
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

    case circulate: {
        double *x1 = malloc(k * sizeof(*x1));
        double *x2 = malloc(k * sizeof(*x2));
        while (with_bm(bench)) {
            clear_array_d(y, k);
            memcpy(x1, x, k * sizeof(*x));
            int i;
            for (i = mpi.rank;
                 i != (mpi.rank + 1) % mpi.size;
                 i = (i - 1 + mpi.size) % mpi.size) {
                MPI_Request reqs[2];
                xtry(MPI_Isend(x1, k, MPI_DOUBLE,
                               (mpi.rank + 1) % mpi.size,
                               0, MPI_COMM_WORLD, reqs + 0));
                xtry(MPI_Irecv(x2, k, MPI_DOUBLE,
                               (mpi.rank - 1 + mpi.size) % mpi.size,
                               0, MPI_COMM_WORLD, reqs + 1));
                cblas_dgemv(CblasRowMajor, CblasNoTrans,
                            k, k, 1., a + k * i, m, x1, 1, 1., y, 1);
                xtry(MPI_Waitall(2, reqs, MPI_STATUSES_IGNORE));
                swap_dp(&x1, &x2);
            }
            cblas_dgemv(CblasRowMajor, CblasNoTrans,
                        k, k, 1., a + k * i, m, x1, 1, 1., y, 1);
        }
        free(x1);
        free(x2);
        break;
    }

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
    return 0;
}
