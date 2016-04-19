#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>
#include "../utils/utils.h"
#include "../utils/mpi.h"

#define NUM_WARMUPS 1
#define NUM_REPEATS 10
#define TICK_FACTOR 10000
#define ROOT_RANK 0
#define EPSILON 1e-12

int main(int argc, char **argv)
{
    const struct mpi mpi = init_mpi(&argc, &argv);

    /* parse args (unsafe) */
    xensure(argc == 4);
    const char *outfile = argv[1];      /* output filename */
    int other = atoi(argv[2]);          /* target rank */
    int n = atoi(argv[3]);              /* number of elements */

    /* redirect stdout to a file because apparently Cray's MPI runner (aprun)
       thought it'd be a good idea to dump diagnostic messages to stdout */
    xtry(!freopen(outfile, "w", stdout));

    double *x = malloc(n * sizeof(*x));
    init_random_array_d(x, n);

    /* initialize benchmark helper */
    parallel_bm parbench;
    bm *bench = init_parallel_bm(&parbench, mpi.rank, ROOT_RANK);
    set_bm_num_repeats(bench, NUM_REPEATS);
    set_bm_num_warmups(bench, NUM_WARMUPS);
    if (mpi.rank == ROOT_RANK) {
        set_bm_time_func(bench, &MPI_Wtime);
        set_bm_preferred_time(bench, MPI_Wtick() * TICK_FACTOR);
    }

    while (with_bm(bench)) {
        if (mpi.rank == ROOT_RANK) {
            xtry(MPI_Send(x, n, MPI_DOUBLE, other,
                          0, MPI_COMM_WORLD));
            xtry(MPI_Recv(x, n, MPI_DOUBLE, other,
                          0, MPI_COMM_WORLD, MPI_STATUS_IGNORE));
        } else if (mpi.rank == other) {
            xtry(MPI_Recv(x, n, MPI_DOUBLE, ROOT_RANK,
                          0, MPI_COMM_WORLD, MPI_STATUS_IGNORE));
            xtry(MPI_Send(x, n, MPI_DOUBLE, ROOT_RANK,
                          0, MPI_COMM_WORLD));
        }
    }

    print_bm_stats(bench, "");

    free(x);
    xtry(MPI_Finalize());
    return 0;
}
