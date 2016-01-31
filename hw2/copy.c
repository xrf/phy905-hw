#include <stdio.h>
#include <stdlib.h>
#include "../utils/utils.h"

void init_random_arrayd(double *array, size_t count)
{
    size_t i;
    for (i = 0; i < count; ++i) {
        array[i] = rand();
    }
}

void copy_arrayd(double *dest, double *src, size_t count)
{
    size_t i;
    for (i = 0; i < count; ++i) {
        dest[i] = src[i];
    }
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
        *i = 0;
        *time = now;
        *count *= 2;
        return 1;
    }
    *time = timediff / *count;
    return 0;
}

int main(void)
{
    size_t k;
    double c[SIZE], a[SIZE];
    struct statistics_state s;
    struct statistics st;
    size_t num_subrepeats = 4;

    mysecond_init();
    init_random_arrayd(a, SIZE);
    statistics_init(&s);

    for (k = 0; k < REPEATS; ++k) {
        size_t j = 0;
        double time = mysecond();
        while (benchmark(&j, &time, &num_subrepeats, 1.)) {
            copy_arrayd(c, a, SIZE);
            dummy(a);
            dummy(c);
        }
        statistics_update(&s, k + 1, time);
    }
    st = statistics_get(&s, k + 1);
    printf("min = %.17g\n"
           "mean = %.17g\n"
           "stdev = %.17g\n"
           "num_subrepeats = %zu\n",
           st.min,
           st.mean,
           st.stdev,
           num_subrepeats);

    return 0;
}
