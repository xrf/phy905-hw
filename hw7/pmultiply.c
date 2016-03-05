#include <stdio.h>
#include <stdlib.h>
#include "../utils/utils.h"

#ifndef VERIFY_THRESHOLD
#define VERIFY_THRESHOLD 1e-11
#endif

static void multiply(double *restrict c,
                     const double *a,
                     const double *b,
                     size_t n)
{
    size_t i;
#ifdef _OPENMP
#   pragma omp parallel for private(i)
#endif
    for (i = 0; i < n; ++i) {
        size_t j, k;
        for (j = 0; j < n; ++j) {
            double sum = 0;
            for (k = 0; k < n; ++k) {
                sum += a[i * n + k] * b[k * n + j];
            }
            c[i * n + j] = sum;
        }
    }
}

static void verify_multiply(const double *restrict c,
                            const double *a,
                            const double *b,
                            size_t n)
{
    size_t i, j, k;
    for (i = 0; i < n; ++i) {
        for (j = 0; j < n; ++j) {
            double c_ij = 0;
            for (k = 0; k < n; ++k) {
                c_ij += a[i * n + k] * b[k * n + j];
            }
            if (!(fabs(c_ij - c[i * n + j]) <= VERIFY_THRESHOLD)) {
                fprintf(stderr,
                        "**INVALID MULTIPLY**\n"
                        "  (%zu, %zu) = %g vs %g\n",
                        i, j, c_ij, c[i * n + j]);
                fflush(stderr);
                exit(EXIT_FAILURE);
            }
        }
    }
}

int main(void)
{
    struct fullbenchmark bench = fullbenchmark_begin_custom(3, 1, 1.);

    const size_t size = getenv_or_i("SIZE", 100);
    double *const buf = (double *)xmalloc(sizeof(*buf) * size * size * 3);
    double *const a = buf + size * size * 0;
    double *const b = buf + size * size * 1;
    double *const c = buf + size * size * 2;
    init_random_array_d(a, size * size);
    init_random_array_d(b, size * size);

    while (fullbenchmark(&bench)) {
        multiply(c, a, b, size);
        dummy(a);
        dummy(b);
        dummy(c);
    }
    verify_multiply(c, a, b, size);
    fullbenchmark_end(&bench);

    free(buf);
    return 0;
}
