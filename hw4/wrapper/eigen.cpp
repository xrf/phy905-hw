#include <eigen3/Eigen/Dense>

extern "C" {

void cblas_dgemm(int x1, int x2, int x3, size_t n, size_t x4, size_t x5,
                 double alpha, const double *a, size_t x6, const double *b,
                 size_t x7, double beta, double *c, size_t x8)
{
    using namespace Eigen;
    Map<const MatrixXd> ma(a, n, n);
    Map<const MatrixXd> mb(b, n, n);
    Map<MatrixXd> mc(c, n, n);
    /* Eigen uses column major so the order is reversed */
    mc = alpha * mb * ma + beta * mc;
}

}
