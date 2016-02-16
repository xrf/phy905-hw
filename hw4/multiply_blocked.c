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
