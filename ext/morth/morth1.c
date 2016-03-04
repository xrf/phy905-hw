#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/times.h>
#include <sys/types.h>
#include <time.h>

#define BASETYPE float
#define VECSIZE 10004
BASETYPE w[VECSIZE], v0[VECSIZE], v1[VECSIZE], v2[VECSIZE], v3[VECSIZE];

void init(int);
void sorth1(int, BASETYPE[]);
void morth1(int);
void morthf(int,BASETYPE [], BASETYPE [], BASETYPE [], BASETYPE [],
	    BASETYPE []);
void morthfr(int,BASETYPE *restrict w, BASETYPE *restrict v0,
	     BASETYPE *restrict v1, BASETYPE *restrict v2,
	     BASETYPE *restrict v3);

/* ISO C90 and SUSv3 require CLOCKS_PER_SEC to be 1,000,000 */
#ifndef CLOCKS_PER_SEC
#define CLOCKS_PER_SEC 1000000
#endif

int main(int argc, char *argv[])
{
    int ntest, k, n;
    clock_t start_t, end_t, clock_dif;
    double  t[5], tval;
    int     ntrial;

    n     = 10000;
    if (argc > 1) n = atoi(argv[1]);
    if (n > VECSIZE-1) {
	fprintf(stderr, "n must be less than %d\n", VECSIZE-1);
	abort();
    }
    ntest = 100000000/n;

    for (k=0; k<5; k++) t[k] = 10000.0;

    /* Run each test multiple times and save the minimum time */
    for (ntrial = 0; ntrial < 3; ntrial++) {
    init(VECSIZE);

    /* Use 4 separate calls to perform the operation */
    start_t = clock();
    for (k=0; k<ntest; k++) {
	sorth1(n,v0);
	sorth1(n,v1);
	sorth1(n,v2);
	sorth1(n,v3);
    }
    end_t = clock(); clock_dif = end_t - start_t;
    tval = (double) (clock_dif/(double)CLOCKS_PER_SEC);
    if (tval < t[0]) t[0] = tval;

    start_t = clock();
    for (k=0; k<ntest; k++) {
	morth1(n);
    }
    end_t = clock(); clock_dif = end_t - start_t;
    tval = (double) (clock_dif/(double)CLOCKS_PER_SEC);
    if (tval < t[1]) t[1] = tval;

    start_t = clock();
    for (k=0; k<ntest; k++) {
	morthf(n,w,v0,v1,v2,v3);
    }
    end_t = clock(); clock_dif = end_t - start_t;
    tval = (double) (clock_dif/(double)CLOCKS_PER_SEC);
    if (tval < t[2]) t[2] = tval;

    start_t = clock();
    for (k=0; k<ntest; k++) {
	morthf(n,w+1,v0+1,v1+1,v2+1,v3+1);
    }
    end_t = clock(); clock_dif = end_t - start_t;
    tval = (double) (clock_dif/(double)CLOCKS_PER_SEC);
    if (tval < t[3]) t[3] = tval;

    start_t = clock();
    for (k=0; k<ntest; k++) {
	morthfr(n,w,v0,v1,v2,v3);
    }
    end_t = clock(); clock_dif = end_t - start_t;
    tval = (double) (clock_dif/(double)CLOCKS_PER_SEC);
    if (tval < t[4]) t[4] = tval;

    }

    /* Report results */
    printf("Times are in seconds and are the cost per array element computed\n");
    printf("n\tsep op  \tin file \tsep file\tw+1     \trestrict\n");
    printf("%d\t%.2e\t%.2e\t%.2e\t%.2e\t%.2e\n", n, t[0]/ntest/n, t[1]/ntest/n,
	t[2]/ntest/n, t[3]/ntest/n, t[4]/ntest/n);

    return 0;
}

void init(int n)
{
    int i;
    double f = n / 6.0;

    for (i=0; i<n; i++) {
	w[i]  = sin((double)i * f);
	v0[i] = 1.0 + f * i;
	v1[i] = cos((double)i * f);
	v2[i] = (i * f) * (i * f);
	v3[i] = sin( (2.0*i) * f );
    }
}

void morth1(int n)
{
    BASETYPE s0 = 0, s1 = 0, s2 = 0, s3 = 0;
    int      i;
    for (i=0; i<n; i++) {
	s0 += w[i] * v0[i];
	s1 += w[i] * v1[i];
	s2 += w[i] * v2[i];
	s3 += w[i] * v3[i];
    }
    for (i=0; i<n; i++) {
	w[i] = w[i] - s0 * v0[i] - s1 * v1[i] - s2 * v2[i] - s3 * v3[i];
    }
}

void sorth1(int n, BASETYPE v[])
{
    BASETYPE s0=0;
    int i;
    for (i=0; i<n; i++) {
	s0 += w[i] * v[i];
    }
    for (i=0; i<n; i++) {
	w[i] = w[i] - s0 * v[i];
    }
}
