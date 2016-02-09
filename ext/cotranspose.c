      
#include <stdio.h>
#include <sys/types.h>
#include <sys/time.h>
#include <stdlib.h>

/* Transpose, assuming column-major (Fortran) storage order (allows direct
   comparison with Fortran routines) */
int transpose( double *a, int ndra, int nr, int nc, double *b, int ndrb )
{
  if (nr < 32) {
    /* perform transpose */
    int i, j, ii;
    double *bb=b;
    const double *aa=a;
    for (j=0; j<nc; j++) {
      ii = 0;
      for (i=0; i<nr; i++) {
	/* b[j+i*ndrb] = a[i+j*ndra]; */
	bb[ii] = aa[i];
	/* Strength reduction */
	ii += ndrb;
      }
      aa += ndra; 
      bb ++;
    }
  }
  else {
    /* subdivide the long side */
    if (nr > nc) {
      transpose( a, ndra, nr/2, nc, b, ndrb );
      transpose( a + nr/2 ,ndra, nr-nr/2, nc, b+(nr/2)*ndrb, ndrb );
    }
    else {
      transpose( a, ndra, nr, nc/2, b, ndrb );
      transpose( a+ndra*(nc/2), ndra, nr, nc-nc/2, b+nc/2, ndrb );
    }
  }
}

int transposeBase( double *a, int ndra, int nr, int nc, double *b, int ndrb )
{
  /* perform transpose */
  int i, j, ii;
  double *bb=b;
  const double *aa=a;
  for (j=0; j<nc; j++) {
    ii = 0;
    for (i=0; i<nr; i++) {
      /* b[j+i*ndrb] = a[i+j*ndra]; */
      bb[ii] = aa[i];
      /* Strength reduction */
      ii += ndrb;
    }
    aa += ndra; 
    bb ++;
  }
}

int main( int argc, char *argv[] )
{
    int matSize=4000, maxTest=10;
    double *matA, *matB;
    int i, j, tests, n;
    int k, rept=10;
    struct timeval  tStart, tEnd;
    float tLoop, t, rate;

    if (argc > 1) {
      matSize = atoi(argv[1]);
    }
    printf( "Transpose %d x %d\n", matSize, matSize );

    n = matSize * matSize;
    matA = (double *) malloc( n * sizeof(double) );
    matB = (double *) malloc( n * sizeof(double) );

    for (i=0; i<n; i++) {
      matA[i] = -i;
      matB[i] = i;
    }

    tLoop = 1.0e10;
    for (tests=0; tests<maxTest; tests++) {
	gettimeofday( &tStart, 0 );
	for (k=0; k<rept; k++) {
	  transpose( matA, matSize, matSize, matSize, matB, matSize );
	}
	gettimeofday( &tEnd, 0 );
	t = (tEnd.tv_sec - tStart.tv_sec) + 
	    1.0e-6 * (tEnd.tv_usec - tStart.tv_usec);
	t = t / rept;
	if (t < tLoop) tLoop = t;
    }
    
    printf( "Time = %f\n", tLoop );
    rate = 8*(matSize*matSize) / tLoop;
    printf( "Rate = %f MB/s\n", rate * 1.0e-6 );

    tLoop = 1.0e10;
    for (tests=0; tests<maxTest; tests++) {
	gettimeofday( &tStart, 0 );
	for (k=0; k<rept; k++) {
	  transposeBase( matA, matSize, matSize, matSize, matB, matSize );
	}
	gettimeofday( &tEnd, 0 );
	t = (tEnd.tv_sec - tStart.tv_sec) + 
	    1.0e-6 * (tEnd.tv_usec - tStart.tv_usec);
	t = t / rept;
	if (t < tLoop) tLoop = t;
    }
    
    printf( "BaseTime = %f\n", tLoop );
    rate = 8*(matSize*matSize) / tLoop;
    printf( "Base Rate = %f MB/s\n", rate * 1.0e-6 );

    free( matA );
    free( matB );

    return 0;
}

