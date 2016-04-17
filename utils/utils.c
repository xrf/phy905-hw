#include <assert.h>
#include <limits.h>
#include <math.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "utils.h"
#include "time.h"

void rf_detailed_abort(const char *prefix,
                       const char *func,
                       int err,
                       const char *msg,
                       const char *expr)
{
    char buf[512];
    char *p = buf;
    size_t n = sizeof(buf) / sizeof(*buf);

    if (!prefix) {
        prefix = "<??" "?>";            /* avoid trigraphs */
    }
    if (!func) {
        func = "<??" "?>";              /* avoid trigraphs */
    }

    /* store it into a buffer before printing to reduce the risk of printing a
       partial message (e.g. when multiple threads are interleaved) */
    rf_snappendf(&p, &n, "%s:%s: [error", prefix, func);
    if (err) {
        rf_snappendf(&p, &n, " %i", err);
    }
    rf_snappendf(&p, &n, "]");
    if (msg) {
        rf_snappendf(&p, &n, " %s", msg);
    }
    if (expr) {
        rf_snappendf(&p, &n, " %s", expr);
    }

    fprintf(stderr, "%s\n", buf);
    fflush(stderr);
    abort();
}

int rf_vsnappendf(char **ptr, size_t *size, const char *format, va_list vlist)
{
    char *const dptr = *ptr;
    const size_t dsize = *size;
    int ret = vsnprintf(dptr, dsize, format, vlist);
    if (ret < 0) {
        /* failed for unknown reasons */
        return ret;
    }
    if ((INT_MAX > (size_t)(-1) && (int)(size_t)ret != ret)
        || (size_t)ret >= dsize) {
        /* output was truncated; return the amount of extra space needed */
        if (dsize) {
            ret -= (int)dsize;
            *ptr = dptr + (dsize - 1);
            *size = 1;
        } else if (ret == INT_MAX) {
            /* avoid overflow (note: reachable only when dsize == 0) */
            return INT_MIN;
        }
        return ret + 1;
    }
    *ptr = dptr + (size_t)ret;
    *size = dsize - (size_t)ret;
    return 0;
}

int rf_snappendf(char **ptr, size_t *size, const char *format, ...)
{
    int ret;
    va_list vlist;
    va_start(vlist, format);
    ret = rf_vsnappendf(ptr, size, format, vlist);
    va_end(vlist);
    return ret;
}

static struct rf_mclock myclock;
static int myclock_initialized;

double min_d(double x, double y)
{
    return
        isnan(x) || isnan(y) ? NAN :
        x < y ? x : y;
}

void *xmalloc(size_t size)
{
    void *p = malloc(size);
    if (!p) {
        abort();
    }
    return p;
}

void init_random_array_d(double *array, size_t count)
{
    size_t i;
    /* not high-quality RNG by any means but good enough for our purposes */
    for (i = 0; i < count; ++i) {
        array[i] = (double)rand() / RAND_MAX - .5;
    }
}

void print_matrix(size_t n, double *a, const char *name)
{
    size_t i, j;
    for (i = 0; i < n; ++i) {
        for (j = 0; j < n; ++j) {
            printf("%s[%zu, %zu]: = %g\n", name, i, j, a[i * n + j]);
        }
    }
    fflush(stdout);
}

int getenv_or_i(const char *name, int value)
{
    const char *s = getenv(name);
    if (!s) {
        return value;
    }
    return atoi(s);
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
        mysecond_init();
    }
    return rf_mclock_getf(&myclock);
}

int benchmark(size_t *i, double *time, size_t *count, double preferred_time)
{
    return benchmark_with(i,
                          time,
                          count,
                          preferred_time,
                          &mysecond,
                          NULL,
                          NULL);
}

int benchmark_with(size_t *i,
                   double *time,
                   size_t *count,
                   double preferred_time,
                   double (*get_time)(void),
                   void (*broadcast)(void *ctx, int *),
                   void *broadcast_ctx)
{
    int keep_going;
    double timediff, now;
    ++*i;
    if (*i < *count) {
        return 1;
    }
    assert(get_time || broadcast);
    if (get_time) {
        now = (*get_time)();
        timediff = now - *time;
        keep_going = timediff < preferred_time;
    }
    if (broadcast) {
        (*broadcast)(broadcast_ctx, &keep_going);
    }
    if (keep_going) {
        /* if it's too short, double the number of repeats */
        *i = 0;
        *count *= 2;
        if (get_time) {
            *time = now;
        }
        return 1;
    }
    if (get_time) {
        *time = timediff / *count;
    }
    return 0;
}

/* ------------------------------------------------------------------------ */

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
    return make_bm(num_repeats);
}

struct fullbenchmark fullbenchmark_begin_custom(size_t num_repeats,
                                                size_t initial_num_subrepeats,
                                                double preferred_time)
{
    struct fullbenchmark self = make_bm(num_repeats);
    set_bm_num_subrepeats(&self, initial_num_subrepeats);
    set_bm_preferred_time(&self, preferred_time);
    return self;
}

int fullbenchmark(struct fullbenchmark *self)
{
    return with_bm(self);
}

void fullbenchmark_end(const struct fullbenchmark *self)
{
    print_bm_stats(self, "");
}

/* ------------------------------------------------------------------------ */

bm make_bm(size_t num_repeats)
{
    bm self;
    self.stats = statistics_initial;
    self.num_repeats = num_repeats;
    self.num_subrepeats = 4;
    self.preferred_time = 1.;
    self.repeat_index = (size_t)(-1);
    self._num_skipped = 0;
    self._get_time = &mysecond;
    self._broadcast = NULL;
    self._broadcast_ctx = NULL;
    mysecond_init();
    return self;
}

void set_bm_time_func(bm *self, double (*get_time)(void))
{
    self->_get_time = get_time;
}

void set_bm_broadcast_func(bm *self,
                           void (*broadcast)(void *ctx, int *),
                           void *broadcast_ctx)
{
    self->_broadcast = broadcast;
    self->_broadcast_ctx = broadcast_ctx;
}

void set_bm_preferred_time(bm *self, double preferred_time)
{
    self->preferred_time = preferred_time;
}

void set_bm_num_warmups(bm *self, size_t num_warmups)
{
    self->num_repeats -= self->_num_skipped;
    self->_num_skipped = num_warmups;
    self->num_repeats += self->_num_skipped;
}

void set_bm_num_subrepeats(bm *self, size_t num_subrepeats)
{
    self->num_subrepeats = num_subrepeats;
}

size_t get_bm_num_subrepeats(const bm *self)
{
    return self->num_subrepeats;
}

int with_bm(bm *self)
{
    if (self->repeat_index == (size_t)(-1)) {
        goto start;
    }
inner:
    if (benchmark_with(&self->subrepeat_index,
                       &self->time,
                       &self->num_subrepeats,
                       self->preferred_time,
                       self->_get_time,
                       self->_broadcast,
                       self->_broadcast_ctx)) {
        return 1;
    }
    if (self->_get_time && self->repeat_index >= self->_num_skipped) {
        statistics_update(&self->stats, self->time);
    }
start:
    ++self->repeat_index;
    if (self->repeat_index < self->num_repeats) {
        self->subrepeat_index = (size_t)(-1);
        if (self->_get_time) {
            self->time = (*self->_get_time)();
        }
        goto inner;
    }
    return 0;
}

void print_bm_stats(const bm *self, const char *prefix)
{
    if (self->_get_time) {
        struct statistics st = statistics_get(&self->stats);
        printf(("%smin = %.17g\n"
                "%smean = %.17g\n"
                "%sstdev = %.17g\n"
                "%snum_subrepeats = %zu\n"),
               prefix,
               st.min,
               prefix,
               st.mean,
               prefix,
               st.stdev,
               prefix,
               get_bm_num_subrepeats(self));
        fflush(stdout);
    }
}
