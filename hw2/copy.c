#include <stdio.h>
#include "../utils/utils.h"
#ifndef SIZE
#define SIZE 250
#endif
#ifndef REPEATS
#define REPEATS 8
#endif

void copy_array_d(double *dest, double *src, size_t count)
{
    size_t i;
    for (i = 0; i < count; ++i) {
        dest[i] = src[i];
    }
}

int main(void)
{
    double c[SIZE], a[SIZE];
    size_t k, num_subrepeats = 4; /* initial guess */
    struct statistics st;
    struct statistics_state s = statistics_initial;
    mysecond_init();
    init_random_array_d(a, SIZE);
    for (k = 0; k < REPEATS; ++k) {
        size_t j = 0;
        double time = mysecond();
        /* repeat until time taken is greater than 1 second */
        while (benchmark(&j, &time, &num_subrepeats, 1.)) {
            copy_array_d(c, a, SIZE);
            dummy(a);
            dummy(c);
        }
        statistics_update(&s, time);
    }
    st = statistics_get(&s);
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
