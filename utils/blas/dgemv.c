#include <assert.h>
#include <cblas.h>

void cblas_dgemv(CBLAS_ORDER layout,
                 CBLAS_TRANSPOSE trans,
                 int m,
                 int n,
                 double alpha,
                 const double *a,
                 int lda,
                 const double *x,
                 int incx,
                 double beta,
                 double *y,
                 int incy)
{
    int i, j;
    (void)layout;
    (void)trans;
    assert(layout == CblasRowMajor);
    assert(trans == CblasNoTrans);
    for (i = 0; i < m; ++i) {
        double s = beta ? beta * y[i * incy] : 0.;
        for (j = 0; j < n; ++j) {
            s += alpha * a[i * lda + j] * x[j * incx];
        }
        y[i * incy] = s;
    }
}
