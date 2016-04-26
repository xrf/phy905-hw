# PHY 905 004 HW #10

<address rel="author">Fei Yuan</address>

I ran the provided code `ioda.c` without doing any customizations on Blue
Waters using the following command:

~~~sh
aprun -n 1024 -N 16 -t 1200 ./ioda 16384 16384 <stripe>
~~~

with `<stripe>` is set to `32`, `16`, and `0`.  Here, `1024` is the total
number of processes, `16` is the number of processes per node, `1200` is the
limit on the number of CPU seconds per process.  None of the jobs exceeded the
time limit.  The `double` arrays were sized `16384 × 16384`.

In the case where `<stripe>` is `0`, running `lfs` on the output files shows:

    lmm_stripe_count: 1

indicating that the file is not striped at all.

The results are shown below:

<figure>
  <table>
    <tr>
      <td>Stripe count</td>
      <td>Open time /s</td>
      <td>Write time /s</td>
      <td>Close time /s</td>
      <td>Rate /(GB/s)</td>
    </tr>
    ${data}
  </table>
  <figcaption>Table 1: Data.</figcaption>
</figure>

The best results were achieved via collective I/O with a stripe count of 32.
The worst results occurred for independent I/O with no striping.  Collective
I/O was generally over a hundred times faster than independent I/O, and
striping further widens the gap.  Striping itself increases the speed by
several factors, and is especially significant for collective I/O.

Also noteworthy is that the time taken to close the file was largely
insignificant, indicating that all the data had been flushed (not necessarily
to disk) before the close occurred.
