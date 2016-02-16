#define CblasRowMajor 0
#define CblasNoTrans 0
#define CblasNoTrans 0
#ifdef __cplusplus
extern "C" {
#endif

void cblas_dgemm(int, int, int, size_t, size_t, size_t,
                 double, const double *, size_t, const double *,
                 size_t, double, double *, size_t);

#ifdef __cplusplus
}
#endif
