#ifndef G_QARUU490A2BZL7I05CXU4ALGQX02A
#define G_QARUU490A2BZL7I05CXU4ALGQX02A
#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    CblasRowMajor = 101
} CBLAS_ORDER;

typedef enum {
    CblasNoTrans = 111
} CBLAS_TRANSPOSE;

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
                 int incy);

#ifdef __cplusplus
}
#endif
#endif
