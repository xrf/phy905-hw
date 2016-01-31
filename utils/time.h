#ifndef G_6NOXAD4UNMA4N8I2GTRMNUZRSRKVW
#define G_6NOXAD4UNMA4N8I2GTRMNUZRSRKVW
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
/** @file

    Time utilities.

    @note     The Windows version of this file needs some testing.
*/

struct rf_mclock {
    uint64_t data;
};

/** Initialize a structure used to access the monotonic wall clock.  The clock
    does not need to be deinitialized.

    @param mclock
    An existing `rf_mclock` structure to be initialized.

    @return
    Zero on success, nonzero on failure.
*/
int rf_mclock_init(struct rf_mclock *mclock);

/** Retrieve the time from a monotonic wall clock in seconds.

    @param mclock
    An `rf_mclock` structure previously initialized by `rf_mclock_init`.

    @return
    Duration relative to some unspecified reference time in seconds.
    If an error occurs, `NAN` is returned.

    Due to the use of double-precision floating point numbers, the precision
    is at worst (for an ideal system with hundreds of years in uptime) limited
    to about a few microseconds.  In practice, it is usually much less.
 */
double rf_mclock_getf(const struct rf_mclock *mclock);

#ifdef __cplusplus
}
#endif
#endif
