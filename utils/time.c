#include <math.h>
#include <stdint.h>
#if defined _WIN32
#include <windows.h>
#elif defined __MACH__
#include <mach/mach_time.h>
#else
#include <time.h>
#include <sys/resource.h>
#endif
#include "time.h"
#ifdef __cplusplus
extern "C" {
#endif

int rf_mclock_init(struct rf_mclock *self)
{
#if defined _WIN32
    LARGE_INTEGER freq;
    if (!QueryPerformanceFrequency(&freq)) {
        return 1;
    }
    *self = (uint64_t)freq.QuadPart;
#elif defined __MACH__
    mach_timebase_info_data_t base;
    if (mach_timebase_info(&base)) {
        return 1;
    }
    *self = (uint64_t)base.numer << 32 | base.denom;
#else
    (void)self;
#endif
    return 0;
}

double rf_mclock_getf(const struct rf_mclock *self)
{
#if defined _WIN32
    LARGE_INTEGER count;
    if (!QueryPerformanceCounter(&count)) {
        return NAN;
    }
    return count.QuadPart / (double)self->data;
#elif defined __MACH__
    uint32_t numer = (uint32_t)(self->data >> 32);
    uint32_t denom = (uint32_t)self->data;
    uint64_t count = mach_absolute_time();
    return (double)count * numer / denom;
#else
    struct timespec t;
    (void)self;
    if (clock_gettime(CLOCK_MONOTONIC, &t)) {
        return NAN;
    }
    return t.tv_sec + t.tv_nsec * 1e-9;
#endif
}

#ifdef __cplusplus
}
#endif
