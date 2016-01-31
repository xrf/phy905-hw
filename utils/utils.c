#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "utils.h"
#include "time.h"

static struct rf_mclock myclock;
static int myclock_initialized;

double min_d(double x, double y)
{
    return
        isnan(x) || isnan(y) ? NAN :
        x < y ? x : y;
}

void init_random_array_d(double *array, size_t count)
{
    size_t i;
    for (i = 0; i < count; ++i) {
        array[i] = rand();
    }
}

/* ------------------------------------------------------------------------ */

void dummy(void *x)
{
    (void)x;
}

void mysecond_init(void)
{
    if (!myclock_initialized) {
        if (rf_mclock_init(&myclock)) {
            fprintf(stderr, "mysecond_init: initialization failed\n");
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
    return rf_mclock_getf(&myclock);
}

int benchmark(size_t *i, double *time, size_t *count, double preferred_time)
{
    double timediff, now;
    ++*i;
    if (*i < *count) {
        return 1;
    }
    now = mysecond();
    timediff = now - *time;
    if (timediff < preferred_time) {
        /* if it's too short, double the number of repeats */
        *i = 0;
        *time = now;
        *count *= 2;
        return 1;
    }
    *time = timediff / *count;
    return 0;
}

/* ------------------------------------------------------------------------ */

struct statistics_state statistics_init()
{
    struct statistics_state self;
    return self;
}

const struct statistics_state statistics_initial = {0, 0, 0, INFINITY};

void statistics_update(struct statistics_state *self, double x)
{
    /* Welford's algorithm for updating mean and standard deviation */
    double mean = self->mean;
    const double delta = x - mean;
    const size_t n = ++self->n;
    mean += delta / n;
    self->mean = mean;
    self->m2 += delta * (x - mean);
    self->min = min_d(self->min, x);
}

struct statistics statistics_get(const struct statistics_state *self)
{
    struct statistics out;
    const size_t n = self->n;
    out.mean = n < 1 ? NAN : self->mean;
    out.stdev = n < 2 ? NAN : sqrt(self->m2 / (n - 1));
    out.min = self->min;
    return out;
}
