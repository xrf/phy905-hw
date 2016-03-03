#include <stdio.h>
#include <stdlib.h>
#include "../utils/utils.h"

void copy_array_d(double *dest, double *src, size_t count)
{
    size_t i;
#   pragma omp parallel for private(i)
    for (i = 0; i < count; ++i) {
        dest[i] = src[i];
    }
}

int main(void)
{
    struct fullbenchmark bench = fullbenchmark_begin_custom(3, 1, 1.);

    const size_t size = getenv_or_i("SIZE", 65536);
    double *buf = (double *)xmalloc(sizeof(*buf) * size * 2);
    double *c = buf + size * 0;
    double *a = buf + size * 1;
    init_random_array_d(a, size);

    while (fullbenchmark(&bench)) {
        copy_array_d(c, a, size);
        dummy(a);
        dummy(c);
    }
    fullbenchmark_end(&bench);

    free(buf);
    return 0;
}
