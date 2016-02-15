#include <stdio.h>
#include <stdlib.h>

#define matSize 1100
#define maxTest 10

/* Row-major order (Same as Fortran).
   
 */
#define ind(i,j) (j)*matSize+i


/* Statically allocate the matrices.  This can improve the compiler's
   ability to optimize operations on these variables.  This will be discussed
   in more detail later in the course. */
double matA[matSize*matSize], matB[matSize*matSize], matC[matSize*matSize];

double second(void);

int main(int argc, char *argv[])
{
    double sum, tStart, tEnd, tLoop, rate, t;
    int    i, j, k, tests;

    /* Initialize the matrics */
    /* Note that this is *not* in the best order with respect to cache;
       this will be discussed later in the course. */
    for (i=0; i<matSize; i++)
	for (j=0; j<matSize; j++) {
	    matA[ind(i,j)] = 1.0 + i;
	    matB[ind(i,j)] = 1.0 + j;
	    matC[ind(i,j)] = 0.0;
	}

    tLoop = 1.0e10;
    for (tests=0; tests<maxTest; tests++) {
	tStart = second();
	for (i=0; i<matSize; i++)
	    for (j=0; j<matSize; j++) {
		sum = 0.0;
		for (k=0; k<matSize; k++)
		    sum += matA[ind(i,k)] * matB[ind(k,j)];
		matC[ind(i,j)] = sum;
	    }
	tEnd = second();
	t = tEnd - tStart;
	if (t < tLoop) tLoop = t;
	if (matC[ind(0,0)] < 0) {
	    fprintf(stderr, "Failed matC sign test\n");
	}
    }

    /* Note that explicit formats are used to limit the number of
       significant digits printed (at most this many digits are significant) */
    printf("Matrix size = %d\n", matSize);
    printf("Time        = %.2e secs\n", tLoop);
    rate = (2.0 * matSize) * matSize * (matSize / tLoop);
    printf("Rate        = %.2e MFLOP/s\n", rate * 1.0e-6);

    return 0;
}

#include <sys/param.h>
#include <sys/types.h>
#include <sys/times.h>
#include <time.h>

double second(void)
{
    long sec;
    double secx;
    struct tms realbuf;

    times(&realbuf);
    secx = ( realbuf.tms_stime + realbuf.tms_utime ) / (float) CLK_TCK;
    return ((double) secx);
}

#if 0
double second(void)
{
}
#endif
