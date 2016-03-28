#ifndef G_AY37CQFF92BMUBCPAX8B8SRSN92PI
#define G_AY37CQFF92BMUBCPAX8B8SRSN92PI
#include <math.h>
#include <stdarg.h>
#include <stddef.h>
#include <stdnoreturn.h>
#ifdef __cplusplus
extern "C" {
#endif

#define rf_stringify_(x) #x
#define rf_stringify(x) rf_stringify_(x)

/** Abort with an error if the expression returns a nonzero value. */
#define rf_xtry(expr)                                                         \
    rf_xtry_(                                                                 \
        (expr),                                                               \
        __FILE__ ":" rf_stringify(__LINE__),                                  \
        __func__,                                                             \
        #expr)

#define rf_xensure(expr)                                                      \
    rf_xensure_(                                                              \
        !!(expr),                                                             \
        __FILE__ ":" rf_stringify(__LINE__),                                  \
        __func__,                                                             \
        #expr)

noreturn
void rf_detailed_abort(const char *prefix,
                       const char *func,
                       int err,
                       const char *msg,
                       const char *expr);

static inline
void rf_xtry_(int err,
              const char *prefix,
              const char *func,
              const char *expr)
{
    if (!err)
        return;
    rf_detailed_abort(prefix, func, err, NULL, expr);
}

static inline
void rf_xensure_(int val,
                 const char *prefix,
                 const char *func,
                 const char *expr)
{
    if (val)
        return;
    rf_detailed_abort(prefix, func, 0, "condition not satisfied:", expr);
}

/** Call `snprintf` on the given buffer, shift the pointer by the length of
    the string written (without the terminating null character), and decrease
    the size by the same amount.  On success, zero is returned.  If the buffer
    is not long enough, the amount of additional buffer space required is
    returned (including the terminating null character).  As with `snprintf`,
    the result is always null-terminated unless the size is zero.  If an error
    occurs, a negative value is returned. */
int rf_snappendf(char **ptr, size_t *size, const char *format, ...);

/** See docs of `snappendf`. */
int rf_vsnappendf(char **ptr, size_t *size,
                  const char *format, va_list vlist);

/* ------------------------------------------------------------------------ */

/** Calculate the minimum of two numbers. */
double min_d(double x, double y);

void *xmalloc(size_t size);

/** Initialize an array of doubles using `rand` (a very weak RNG). */
void init_random_array_d(double *array, size_t count);

/** Print a square matrix with the given name. */
void print_matrix(size_t dim, double *matrix, const char *name);

int getenv_or_i(const char *name, int value);

/* ------------------------------------------------------------------------ */

/** A no-op function used to suppress certain optimizations. */
void dummy(void *);

/** Initialize the global clock.  Must be called before mysecond. */
void mysecond_init(void);

/** Obtain the number of seconds elapsed on a monotonic wall clock.  The time
    of reference is arbitrary. */
double mysecond(void);

/** Helper function for repeating a calculation until the total time taken is
    at least `preferred_time` seconds.  Note: `i` should be initialized to
    `(size_t)(-1)`. */
int benchmark(size_t *i, double *time, size_t *count, double preferred_time);

/* ------------------------------------------------------------------------ */

/** Contains the mean, standard deviation, and minimum. */
struct statistics {
    double mean, stdev, min;
};

/** For tracking the state of an incremental statistics calculator. */
struct statistics_state {
    size_t n;
    double mean, m2, min;
};

/** Initial state. */
extern const struct statistics_state statistics_initial;

/** Add another value and update the statistics. */
void statistics_update(struct statistics_state *self, double x);

/** Obtain the statistics from the given state. */
struct statistics statistics_get(const struct statistics_state *self);

/* ------------------------------------------------------------------------ */

struct fullbenchmark {
    struct statistics_state stats;
    size_t num_repeats, num_subrepeats, repeat_index, subrepeat_index;
    double time, preferred_time;
};

struct fullbenchmark fullbenchmark_begin(size_t num_repeats);

struct fullbenchmark fullbenchmark_begin_custom(size_t num_repeats,
                                                size_t initial_num_subrepeats,
                                                double preferred_time);

int fullbenchmark(struct fullbenchmark *self);

void fullbenchmark_end(const struct fullbenchmark *self);

#ifdef __cplusplus
}
#endif
#endif
