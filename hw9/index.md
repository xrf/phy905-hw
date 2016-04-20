# PHY 905 004 HW #9

<address rel="author">Fei Yuan</address>

Notation:

  - `M` is the dimension of the matrix.
  - `p` is the number of processes.
  - `c` is the cost of a single floating-point operation.
  - `m` is the cost of reading from RAM.
  - `r` is the cost of moving data via MPI.

## Method 1 (using `MPI_Allgather`):

The matrix-vector product involves computing `M^2 / p` multiplications and additions, reading `2 × M^2 / p` elements (neglecting cache, so the vector is re-read `M / p` times), and storing `M` elements.  Considering only leading order effects, this gives us:

~~~equation
2 × (M^2 / p) × (c + 8 B × m)
~~~

The `MPI_Allgather` involves the receiving `M / p` elements from `p - 1` processes and then sending `M / p` to `p - 1` processes.  The dominant term is thus:

~~~equation
2 × M × 8 B × r
~~~

## Method 2 (circulating the vector elements in a ring):

The matrix-vector product involves computing `M^2 / p^2` multiplications and additions, reading `2 × M^2 / p^2` elements (neglecting cache), and storing `M / p` elements, all of which are repeated `p` times.  Considering only leading order effects, this gives us:

~~~equation
2 × (M^2 / p) × (c + 8 B × m)
~~~

Each circulation involves sending `M / p` elements to the next process and receiving `M / p` elements from the previous process, all of which are repeated `p - 1` times.  The dominant term is thus:

~~~equation
2 × M × 8 B × r
~~~

## Analysis

So it turns out that both methods have the same cost in this simple model where we only consider throughput.  We set the following parameters:

  - `r = 1.5 GB/s`, empirically measured on Blue Waters
  - `m = 5 GB/s`, an order-of-magnitude guess based on typical RAM specs
  - `c = 4 GFLOPS`, an order-of-magnitude guess based on typical CPU specs

For the graphs, we plot the following model with the parameters above:

~~~equation
2 × (M^2 / p) × (c + 8 B × m) + 2 × M × 8 B × r
~~~

We find that the communication cost is rather insignificant compared to the calculation cost provided that `p ≪ M × r / (c / 8 B + m)`.  This holds for most of the test cases except when `M = 1024`.

<figure>
  <a href="${fig_time_fn}"><img src="${fig_time_fn}"/></a>
  <figcaption>Figure 1: Time vs number of MPI processes.</figcaption>
</figure>

The result was not quite what I expected based on the model.  The model follows the overall trend for the larger two sizes but appears to be several factors off, perhaps due to the wrong choice of the parameters.  The model does not predict the trend for the smallest size where `M = 1024` very well, and is especially poor for the second method, where the time seems to *increase* with the number of processes.  This suggests there is some sort of overhead that is amplified as the number of processes increase – perhaps the overhead of sending and receiving MPI messages, which was not taken into account.

For the test cases performed, method 2 is generally slower than method 1, and becomes even worse as the size of the array decreases.  Interleaving the communication with the calculation does not seem to aid the performance.  A possible explanation is that:

  - For smaller matrices, the overhead of sending lots of tiny messages is very high compared to the computation.
  - For larger matrices, the interleaving does not really offer any benefit since the communication cost is negligible compared to the computation cost.

It seems that method 1 is always the best choice, albeit requiring a slightly higher memory usage.

<figure>
  <table>
    <tr>
      <td>Method</td>
      <td><code>p</code></td>
      <td><code>M</code></td>
      <td>Time /s</td>
    </tr>
    ${data}
  </table>
  <figcaption>Table 1: Data.</figcaption>
</figure>
