#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mpi.h>
#include "../utils/utils.h"
#define xtry(x) rf_xtry(x)
#define xensure(x) rf_xensure(x)

#define WARMUP_REPEATS 1
#define NUM_REPEATS 10
#define TICK_FACTOR 10000

/** Initialize MPI and return the rank. */
static int init_mpi(int *argc, char ***argv)
{
    int rank, provided, required = MPI_THREAD_FUNNELED;
    xtry(MPI_Init_thread(argc, argv, required, &provided));
    xensure(provided >= required);
    xtry(MPI_Comm_rank(MPI_COMM_WORLD, &rank));
    return rank;
}

/** Some arbitrary pattern in the data. */
static unsigned char some_data(size_t index, int rank)
{
    return (unsigned char)(index + rank);
}

static void init_data(unsigned char *data, size_t size, int rank)
{
    for (size_t i = 0; i < size; ++i) {
        data[i] = some_data(i, rank);
    }
}

/** Ensure the data was transmitted intact. */
static void verify_data(unsigned char *data, size_t size, int rank)
{
    for (size_t i = 0; i < size; ++i) {
        assert(data[i] == some_data(i, rank));
    }
}

/** Ping-pong test using blocking primitives. */
static void pingpong(int is_master,
                     const void *sendbuf,
                     void *recvbuf,
                     size_t m,
                     int other)
{
    if (is_master) {
        xtry(MPI_Send(sendbuf, m, MPI_UNSIGNED_CHAR, other,
                      0, MPI_COMM_WORLD));
        xtry(MPI_Recv(recvbuf, m, MPI_UNSIGNED_CHAR, other,
                      MPI_ANY_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE));
    } else {
        xtry(MPI_Recv(recvbuf, m, MPI_UNSIGNED_CHAR, other,
                      MPI_ANY_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE));
        xtry(MPI_Send(sendbuf, m, MPI_UNSIGNED_CHAR, other,
                      0, MPI_COMM_WORLD));
    }
}

/** Ping-pong test using nonblocking primitives. */
static void ipingpong(int is_master,
                      const void *sendbuf,
                      void *recvbuf,
                      size_t m,
                      int other)
{
    MPI_Request request;
    if (is_master) {
        xtry(MPI_Isend(sendbuf, m, MPI_UNSIGNED_CHAR, other,
                       0, MPI_COMM_WORLD, &request));
        xtry(MPI_Wait(&request, MPI_STATUS_IGNORE));
        xtry(MPI_Irecv(recvbuf, m, MPI_UNSIGNED_CHAR, other,
                       MPI_ANY_TAG, MPI_COMM_WORLD, &request));
        xtry(MPI_Wait(&request, MPI_STATUS_IGNORE));
    } else {
        xtry(MPI_Irecv(recvbuf, m, MPI_UNSIGNED_CHAR, other,
                       MPI_ANY_TAG, MPI_COMM_WORLD, &request));
        xtry(MPI_Wait(&request, MPI_STATUS_IGNORE));
        xtry(MPI_Isend(sendbuf, m, MPI_UNSIGNED_CHAR, other,
                       0, MPI_COMM_WORLD, &request));
        xtry(MPI_Wait(&request, MPI_STATUS_IGNORE));
    }
}

/** Head-to-head ping-pong test. */
static void hhpingpong(int is_master,
                       const void *sendbuf,
                       void *recvbuf,
                       size_t m,
                       int other)
{
    MPI_Request recvreq, sendreq;
    xtry(MPI_Isend(sendbuf, m, MPI_UNSIGNED_CHAR, other,
                   0, MPI_COMM_WORLD, &sendreq));
    xtry(MPI_Irecv(recvbuf, m, MPI_UNSIGNED_CHAR, other,
                   MPI_ANY_TAG, MPI_COMM_WORLD, &recvreq));
    if (is_master) {
        xtry(MPI_Wait(&sendreq, MPI_STATUS_IGNORE));
        xtry(MPI_Wait(&recvreq, MPI_STATUS_IGNORE));
    } else {
        xtry(MPI_Wait(&recvreq, MPI_STATUS_IGNORE));
        xtry(MPI_Wait(&sendreq, MPI_STATUS_IGNORE));
    }
}

/** Repeat the pingpong benchmark the given number of times. */
static double subbench_pingpong(int is_master,
                             const unsigned char *sendbuf,
                             unsigned char *recvbuf,
                             size_t m,
                             int other,
                             void (*pingpong)(int,
                                              const void *,
                                              void *,
                                              size_t,
                                              int),
                             uint64_t numrepeats)
{
    const double t0 = MPI_Wtime();
    for (uint64_t i = 0; i < numrepeats; ++i) {
        (*pingpong)(is_master, sendbuf, recvbuf, m, other);
    }
    return MPI_Wtime() - t0;
}

/** Perform pingpong benchmark the enough times to get a reliable result. */
static void bench_pingpong(int is_master,
                           const unsigned char *sendbuf,
                           unsigned char *recvbuf,
                           size_t m,
                           int other,
                           void (*pingpong)(int,
                                            const void *,
                                            void *,
                                            size_t,
                                            int),
                           const char *suffix,
                           double mintime)
{
    uint64_t numsubrepeats = 1;
    uint64_t bestnumsubrepeats = -1;
    double besttime = INFINITY;

    /* avoid the first few tests, as they tend to be outliers */
    for (uint64_t r = 0; r < WARMUP_REPEATS; ++r) {
        subbench_pingpong(is_master, sendbuf, recvbuf, m,
                          other, pingpong, numsubrepeats);
    }

    for (uint64_t r = 0; r < NUM_REPEATS; ++r) {

        double time;
        while (1) {
            time = subbench_pingpong(is_master, sendbuf, recvbuf, m,
                                     other, pingpong, numsubrepeats);
            int should_break;
            if (is_master) {
                should_break = time >= mintime;
                xtry(MPI_Send(&should_break, 1, MPI_INT, other,
                              0, MPI_COMM_WORLD));
            } else {
                xtry(MPI_Recv(&should_break, 1, MPI_INT, other,
                              MPI_ANY_TAG, MPI_COMM_WORLD, MPI_STATUS_IGNORE));
            }
            if (should_break) {
                break;
            }
            numsubrepeats *= 2;
        }

        if (is_master) {
            time /= numsubrepeats;
            printf("time_%s_%zu /s = %.17g\n", suffix, r, time);
            if (time < besttime) {
                besttime = time;
                bestnumsubrepeats = numsubrepeats;
            }
        }
    }

    if (is_master) {
        printf("time_%s /s = %.17g\n", suffix, besttime);
        printf("numsubrepeats_%s = %zu\n", suffix, bestnumsubrepeats);
    }

    verify_data(recvbuf, m, other);
    memset(recvbuf, 0, m);
}

static void bench_all(int is_master,
                      const unsigned char *sendbuf,
                      unsigned char *recvbuf,
                      size_t m,
                      int other,
                      double mintime)
{
    bench_pingpong(is_master, sendbuf, recvbuf, m, other,
                   pingpong, "1a", mintime);
    bench_pingpong(is_master, sendbuf, recvbuf, m, other,
                   ipingpong, "1b", mintime);
    bench_pingpong(is_master, sendbuf, recvbuf, m, other,
                   hhpingpong, "2a", mintime);
}

int main(int argc, char **argv)
{
    const int rank = init_mpi(&argc, &argv);

    /* parse args (unsafe) */
    xensure(argc > 3);
    int i = atoi(argv[1]);
    int j = atoi(argv[2]);
    size_t m = atoi(argv[3]);

    unsigned char *buf = calloc((m ? m : 1) * 2, 1);
    xensure(buf);
    unsigned char *sendbuf = buf;
    unsigned char *recvbuf = buf + (m ? m : 1);
    init_data(sendbuf, m, rank);

    if (rank == i) {
        double tick = MPI_Wtick();
        printf("tick /s = %.17g\n", tick);
        double min_time = tick * TICK_FACTOR;
        printf("min_time /s = %.17g\n", min_time);
        bench_all(1, sendbuf, recvbuf, m, j, min_time);
    } else if (rank == j) {
        bench_all(0, sendbuf, recvbuf, m, i, NAN);
    }

    xtry(MPI_Finalize());
    free(buf);
}
