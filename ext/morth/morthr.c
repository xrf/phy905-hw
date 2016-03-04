#define BASETYPE float

void morthf(int n, BASETYPE w[], BASETYPE v0[], BASETYPE v1[], BASETYPE v2[],
    BASETYPE v3[])
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

void morthfr(int n, BASETYPE * restrict w,
	     const BASETYPE * restrict v0,
	     const BASETYPE * restrict v1,
	     const BASETYPE * restrict v2,
	     const BASETYPE * restrict v3)
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
