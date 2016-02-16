#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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

static void multiply(size_t n, double *restrict c,
                     const double *a, const double *b)
{
#if BSIZE < 2
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
    memset(c, 0, n * n * sizeof(*c));
    size_t ni1;
    for (size_t i = 0; i != n; i = ni1) {
        ni1 = i + BSIZE;
        if (ni1 > n) {
            ni1 = n;
        }
        size_t nj1;
        for (size_t j = 0; j != n; j = nj1) {
            nj1 = j + BSIZE;
            if (nj1 > n) {
                nj1 = n;
            }
            for (size_t k = 0; k != n; ++k) {
                for (size_t i1 = i; i1 != ni1; ++i1) {
                    for (size_t j1 = j; j1 != nj1; ++j1) {
                        c[i1 * n + j1] += a[i1 * n + k] * b[k * n + j1];
                    }
                }
            }
        }
    }
#endif
}

static void verify_multiply(size_t n, const double *restrict c,
                            const double *a, const double *b)
{
    static const double epsilon = 0;
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            double c_ij = 0;
            for (size_t k = 0; k < n; ++k) {
                c_ij += a[i * n + k] * b[k * n + j];
            }
            if (!(fabs(c_ij - c[i * n + j]) <= epsilon)) {
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
