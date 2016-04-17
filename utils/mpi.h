#ifndef G_0OPL73W4MUO995T5NWYK0TGHVE3CV
#define G_0OPL73W4MUO995T5NWYK0TGHVE3CV
#include "utils.h"
#ifdef __cplusplus
extern "C" {
#endif

struct mpi {
    int rank, size;
};

/** Initialize MPI and return the rank and world size. */
struct mpi init_mpi(int *argc, char ***argv);

typedef struct {
    bm _bench;
    int _root;
} parallel_bm;

bm *init_parallel_bm(parallel_bm *, int rank, int root, size_t num_repeats);

bm *parallel_bm_as_bm(parallel_bm *);

#ifdef __cplusplus
}
#endif
#endif
