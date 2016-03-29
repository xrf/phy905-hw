from makegen import *

NAME = "mpicomm"
SIZES = [0] + [2 ** k for k in range(2, 19)]
PROCS = ["0 1", "0 `expr $(WSIZE) - 1`", "2 3"]

b = RelocatedBuilder(root="..")
build = b.build_program(
    NAME,
    [
        b.compile_source(NAME + ".c"),
        b.compile_source("../utils/utils.c"),
        b.compile_source("../utils/time.c"),
    ],
    libraries="$(LIBS)",
)

benchs = [simple_command(
    "mpiexec -np $(WSIZE) {0} " + ps + " " + str(size) +
    " | tee {out}.tmp && mv {out}.tmp {out}",
    "bench_{0}_{1:06}.txt".format(ips + 1, size),
    [build],
) for ips, ps in enumerate(PROCS) for size in SIZES]

analysis = simple_command(
    "python {0} analyze {out} {all1}",
    "analysis.json",
    ["main.py"] + benchs,
)

plot = simple_command(
    "python {0} plot {out} {all1}",
    "figs.json",
    ["main.py", analysis],
)

report = simple_command(
    "python {0} report {out} {all1}",
    "index.html",
    ["main.py", analysis, plot, "template.html"],
)

makefile = alias("all", [report]).merge(
    alias("bench", benchs),
    Ruleset(macros={
        "CC": "mpicc",
        "CFLAGS": "-Wall -Wextra -O3 -g",
        "LIBS": "-lm",
        "WSIZE": "4",
    }),
)

makefile.save()
