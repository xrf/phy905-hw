#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "utils.h"
#include "time.h"
#ifdef __cplusplus
extern "C" {
#endif

static struct lt_mclock myclock;
static int myclock_initialized;

void dummy(void *x)
{
    (void)x; /* unused */
}

void mysecond_init(void)
{
    if (!myclock_initialized) {
        if (lt_mclock_init(&myclock)) {
            fprintf(stderr, "init_clock: initialization failed\n");
            fflush(stderr);
            abort();
        }
        myclock_initialized = 1;
    }
}

double mysecond(void)
{
    if (!myclock_initialized) {
        fprintf(stderr, "mysecond: clock has not yet been initialized\n");
        fflush(stderr);
        abort();
    }
    return lt_mclock_getf(&myclock);
    /* return clock() / (double)CLOCKS_PER_SEC; */
}

void statistics_init(struct statistics_state *self)
{
    self->mean = 0;
    self->m2 = 0;
    self->min = INFINITY;
}

void statistics_update(struct statistics_state *self, size_t n, double x)
{
    /* Welford's algorithm for updating mean and standard deviation */
    double mean = self->mean;
    const double delta = x - mean;
    mean += delta / n;
    self->mean = mean;
    self->m2 += delta * (x - mean);
    self->min = min_d(self->min, x);
}

struct statistics statistics_get(const struct statistics_state *self, size_t n)
{
    struct statistics out;
    out.mean = n < 1 ? NAN : self->mean;
    out.stdev = n < 2 ? NAN : sqrt(self->m2 / (n - 1));
    out.min = self->min;
    return out;
}

#ifdef __cplusplus
}
#endif
