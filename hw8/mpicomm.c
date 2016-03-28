#include <assert.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>
#include "../utils/utils.h"
#define xtry(x) rf_xtry(x)
#define xensure(x) rf_xensure(x)

#define WARMUP_REPEATS 1
#define TICK_FACTOR 10000

static int init_mpi(int *argc, char ***argv)
{
    int rank, provided, required = MPI_THREAD_FUNNELED;
    xtry(MPI_Init_thread(argc, argv, required, &provided));
    xensure(provided >= required);
    xtry(MPI_Comm_rank(MPI_COMM_WORLD, &rank));
    return rank;
}

static void verify_and_reset(unsigned char *sendbuf,
                             unsigned char *recvbuf,
                             size_t m,
                             int other)
{
    for (unsigned char *p = recvbuf + 1; p != recvbuf + m; ++p) {
        assert(*p == (unsigned char)(p - recvbuf + other));
    }
    memset(recvbuf, 0, m);
    sendbuf[0] = 0;
}

static void pingpong(unsigned char *sendbuf,
                     unsigned char *recvbuf,
                     size_t m,
                     int other)
{
    xtry(MPI_Send(sendbuf, m, MPI_CHAR, other, 0, MPI_COMM_WORLD));
    xtry(MPI_Recv(recvbuf, m, MPI_CHAR, other, MPI_ANY_TAG,
                  MPI_COMM_WORLD, MPI_STATUS_IGNORE));
}

static void ipingpong(unsigned char *sendbuf,
                      unsigned char *recvbuf,
                      size_t m,
                      int other)
{
    MPI_Request request;
    xtry(MPI_Isend(sendbuf, m, MPI_CHAR, other, 0, MPI_COMM_WORLD, &request));
    xtry(MPI_Wait(&request, MPI_STATUS_IGNORE));
    xtry(MPI_Irecv(recvbuf, m, MPI_CHAR, other, MPI_ANY_TAG,
                   MPI_COMM_WORLD, &request));
    xtry(MPI_Wait(&request, MPI_STATUS_IGNORE));
}

static void pongping(unsigned char *sendbuf,
                     unsigned char *recvbuf,
                     size_t m,
                     int other)
{
    xtry(MPI_Recv(recvbuf, m, MPI_CHAR, other, MPI_ANY_TAG,
                  MPI_COMM_WORLD, MPI_STATUS_IGNORE));
    xtry(MPI_Send(sendbuf, m, MPI_CHAR, other, 0, MPI_COMM_WORLD));
}

static void ipongping(unsigned char *sendbuf,
                      unsigned char *recvbuf,
                      size_t m,
                      int other)
{
    MPI_Request request;
    xtry(MPI_Irecv(recvbuf, m, MPI_CHAR, other, MPI_ANY_TAG,
                   MPI_COMM_WORLD, &request));
    xtry(MPI_Wait(&request, MPI_STATUS_IGNORE));
    xtry(MPI_Isend(sendbuf, m, MPI_CHAR, other, 0, MPI_COMM_WORLD, &request));
    xtry(MPI_Wait(&request, MPI_STATUS_IGNORE));
}

static void hhpingpong(unsigned char *sendbuf,
                       unsigned char *recvbuf,
                       size_t m,
                       int other)
{
    MPI_Request recvreq, sendreq;
    xtry(MPI_Isend(sendbuf, m, MPI_CHAR, other, 0, MPI_COMM_WORLD, &sendreq));
    xtry(MPI_Irecv(recvbuf, m, MPI_CHAR, other, MPI_ANY_TAG,
                   MPI_COMM_WORLD, &recvreq));
    xtry(MPI_Wait(&sendreq, MPI_STATUS_IGNORE));
    xtry(MPI_Wait(&recvreq, MPI_STATUS_IGNORE));
}

static void hhpongping(unsigned char *sendbuf,
                       unsigned char *recvbuf,
                       size_t m,
                       int other)
{
    MPI_Request recvreq, sendreq;
    xtry(MPI_Isend(sendbuf, m, MPI_CHAR, other, 0, MPI_COMM_WORLD, &sendreq));
    xtry(MPI_Irecv(recvbuf, m, MPI_CHAR, other, MPI_ANY_TAG,
                   MPI_COMM_WORLD, &recvreq));
    xtry(MPI_Wait(&recvreq, MPI_STATUS_IGNORE));
    xtry(MPI_Wait(&sendreq, MPI_STATUS_IGNORE));
}

static void bench_i(unsigned char *sendbuf,
                    unsigned char *recvbuf,
                    size_t m,
                    int other,
                    void (*pingpong)(unsigned char *,
                                     unsigned char *,
                                     size_t,
                                     int),
                    const char *suffix,
                    double min_time)
{
    int k = 0;
    double t = 0;

    for (size_t r = 0; r != WARMUP_REPEATS; ++r) {
        (*pingpong)(sendbuf, recvbuf, m, other);
    }

    const double t0 = MPI_Wtime();
    do {
        (*pingpong)(sendbuf, recvbuf, m, other);
        t = MPI_Wtime() - t0;
        ++k;
    } while (t < min_time);

    /* tell the other process to stop */
    sendbuf[0] = 1;
    (*pingpong)(sendbuf, recvbuf, m, other);

    printf("time_%s /s = %.17g\n", suffix, t / k);
    printf("repeats_%s = %i\n", suffix, k);

    verify_and_reset(sendbuf, recvbuf, m, other);
}

static void bench_j(unsigned char *sendbuf,
                    unsigned char *recvbuf,
                    size_t m,
                    int other,
                    void (*pongping)(unsigned char *,
                                     unsigned char *,
                                     size_t,
                                     int))
{
    do {
        (*pongping)(sendbuf, recvbuf, m, other);
    } while (!recvbuf[0]);
    verify_and_reset(sendbuf, recvbuf, m, other);
}

int main(int argc, char **argv)
{
    const int rank = init_mpi(&argc, &argv);

    /* parse args (unsafe) */
    xensure(argc > 3);
    int i = atoi(argv[1]);
    int j = atoi(argv[2]);
    size_t m = atoi(argv[3]);

    unsigned char *buf = calloc(m * 2, 1);
    xensure(buf);
    unsigned char *sendbuf = buf;
    unsigned char *recvbuf = buf + m;

    /* initialize buffer (note: 1st element is used for control purposes) */
    for (unsigned char *p = sendbuf + 1; p != sendbuf + m; ++p) {
        *p = (unsigned char)(p - sendbuf + rank);
    }

    if (rank == i) {

        double tick = MPI_Wtick();
        printf("tick /s = %.17g\n", tick);
        double min_time = tick * TICK_FACTOR;
        printf("min_time /s = %.17g\n", min_time);

        bench_i(sendbuf, recvbuf, m, j, pingpong, "1A", min_time);
        bench_i(sendbuf, recvbuf, m, j, ipingpong, "1b", min_time);
        bench_i(sendbuf, recvbuf, m, j, hhpingpong, "2a", min_time);

    } else if (rank == j) {

        bench_j(sendbuf, recvbuf, m, i, pongping);
        bench_j(sendbuf, recvbuf, m, i, ipongping);
        bench_j(sendbuf, recvbuf, m, i, hhpongping);

    }

    xtry(MPI_Finalize());
    free(buf);
}
