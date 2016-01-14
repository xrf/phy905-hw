#include <time.h>

double mysecond(void)
{
    return clock() / (double)CLOCKS_PER_SEC;
}
