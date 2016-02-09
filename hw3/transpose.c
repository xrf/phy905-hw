#include <stdio.h>
#include <stdlib.h>
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

static void transpose(size_t n, double *b, const double *a)
{
#if BSIZE < 2
    size_t i, j;
    for (i = 0; i < n; ++i) {
        for (j = 0; j < n; ++j) {
            b[j * n + i] = a[i * n + j];
        }
    }
#else
    size_t i, j, i1, j1, ni1, nj1;
    for (i = 0; i != n; i = ni1) {
        ni1 = i + BSIZE;
        if (n < ni1) {
            ni1 = n;
        }
        for (j = 0; j != n; j = nj1) {
            nj1 = j + BSIZE;
            if (n < nj1) {
                nj1 = n;
            }
            for (i1 = i; i1 != ni1; ++i1) {
                for (j1 = j; j1 != nj1; ++j1) {
                    b[j1 * n + i1] = a[i1 * n + j1];
                }
            }
        }
    }
#endif
}

static void verify_transpose(size_t n, const double *a, const double *b)
{
    for (size_t i = 0; i < n; ++i) {
        for (size_t j = 0; j < n; ++j) {
            if (a[i * n + j] != b[j * n + i]) {
                fprintf(stderr, "**INVALID TRANSPOSE**\n");
                fflush(stderr);
                exit(EXIT_FAILURE);
            }
        }
    }
}

int main(void)
{
    struct fullbenchmark bench = fullbenchmark_begin(REPEATS);
    double a[SIZE * SIZE], b[SIZE * SIZE];
    init_random_array_d(a, sizeof(a) / sizeof(*a));
    while (fullbenchmark(&bench)) {
        transpose(SIZE, b, a);
        dummy(a);
        dummy(b);
    }
    verify_transpose(SIZE, a, b);
    fullbenchmark_end(&bench);
    return 0;
}
