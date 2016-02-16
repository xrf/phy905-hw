#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef USE_BLAS
#include <cblas.h>
#endif
#include "../utils/utils.h"
#ifndef SIZE
#define SIZE 20
#endif
#ifndef BSIZE
#define BSIZE 1
#endif
#ifndef REPEATS
#define REPEATS 8
#endif
#ifndef VERIFY_THRESHOLD
#define VERIFY_THRESHOLD 1e-12
#endif

static void multiply(size_t n, double *restrict c,
                     const double *a, const double *b)
{
#if defined USE_BLAS
    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, n, n, n, 1., a, n, b, n, 0., c, n);
#elif BSIZE < 2
    for (size_t i = 0; i != n; ++i) {
        for (size_t j = 0; j != n; ++j) {
            double sum = 0;
            for (size_t k = 0; k != n; ++k) {
                sum += a[i * n + k] * b[k * n + j];
            }
            c[i * n + j] = sum;
        }
    }
#else
#include "multiply_blocked.c"
#endif
}

static void verify_multiply(size_t n, const double *restrict c,
                            const double *a, const double *b)
{
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            double c_ij = 0;
            for (size_t k = 0; k < n; ++k) {
                c_ij += a[i * n + k] * b[k * n + j];
            }
            if (!(fabs(c_ij - c[i * n + j]) <= VERIFY_THRESHOLD)) {
                fprintf(stderr, "**INVALID MULTIPLY**\n  (%zu, %zu) = %g vs %g\n",
                        i, j, c_ij, c[i * n + j]);
                fflush(stderr);
                exit(EXIT_FAILURE);
            }
        }
    }
}

int main(void)
{
    struct fullbenchmark bench = fullbenchmark_begin(REPEATS);
    double a[SIZE * SIZE], b[SIZE * SIZE], c[SIZE * SIZE];
    init_random_array_d(a, sizeof(a) / sizeof(*a));
    init_random_array_d(b, sizeof(b) / sizeof(*b));
    while (fullbenchmark(&bench)) {
        multiply(SIZE, c, a, b);
        dummy(a);
        dummy(b);
    }
    verify_multiply(SIZE, c, a, b);
    fullbenchmark_end(&bench);
    return 0;
}
