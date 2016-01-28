#ifndef G_AY37CQFF92BMUBCPAX8B8SRSN92PI
#define G_AY37CQFF92BMUBCPAX8B8SRSN92PI
#include <math.h>
#ifdef __cplusplus
extern "C" {
#endif

static inline double min_d(double x, double y)
{
    return
        isnan(x) || isnan(y) ? NAN :
        x < y ? x : y;
}

/* Used to suppress certain optimizations */
void dummy(void *);

/* Initialize the global clock.  Must be called before mysecond. */
void mysecond_init(void);

double mysecond(void);

struct statistics {
    double mean, stdev, min;
};

struct statistics_state {
    double mean, m2, min;
};

void statistics_init(struct statistics_state *self);

void statistics_update(struct statistics_state *self, size_t n, double x);

struct statistics statistics_get(const struct statistics_state *self, size_t n);

#ifdef __cplusplus
}
#endif
#endif
