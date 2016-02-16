#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "utils.h"
#include "time.h"
#ifndef PREFERRED_TIME
#define PREFERRED_TIME 1.
#endif
#ifndef MIN_SUBREPEATS /* initial guess */
#define MIN_SUBREPEATS 4
#endif

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
    /* not high-quality RNG by any means but good enough for our purposes */
    for (i = 0; i < count; ++i) {
        array[i] = (double)rand() / RAND_MAX;
    }
}

void print_matrix(size_t n, double *a, const char *name)
{
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            printf("%s[%zu, %zu]: = %g\n", name, i, j, a[i * n + j]);
        }
    }
    fflush(stdout);
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

/* ------------------------------------------------------------------------ */

struct fullbenchmark fullbenchmark_begin(size_t num_repeats)
{
    struct fullbenchmark self;
    mysecond_init();
    self.stats = statistics_initial;
    self.num_repeats = num_repeats;
    self.num_subrepeats = MIN_SUBREPEATS;
    self.repeat_index = 0;
    self.first = 1;
    return self;
}

int fullbenchmark(struct fullbenchmark *self)
{
    if (self->first) {
        self->first = 0;
        goto first;
    }
inner:
    if (benchmark(&self->subrepeat_index, &self->time,
                  &self->num_subrepeats, PREFERRED_TIME)) {
        return 1;
    }
    statistics_update(&self->stats, self->time);
    ++self->repeat_index;
first:
    if (self->repeat_index < self->num_repeats) {
        self->subrepeat_index = (size_t)(-1);
        self->time = mysecond();
        goto inner;
    }
    return 0;
}

void fullbenchmark_end(const struct fullbenchmark *self)
{
    struct statistics st = statistics_get(&self->stats);
    printf("min = %.17g\n"
           "mean = %.17g\n"
           "stdev = %.17g\n"
           "num_subrepeats = %zu\n",
           st.min,
           st.mean,
           st.stdev,
           self->num_subrepeats);
    fflush(stdout);
}
