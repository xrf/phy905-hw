from makegen import *
import glob

NAME = "mpigemv"

b = RelocatedBuilder(root="..")
build = b.build_program(
    NAME,
    [
        b.compile_source(NAME + ".c"),
        b.compile_source("../utils/mpi.c"),
        b.compile_source("../utils/time.c"),
        b.compile_source("../utils/utils.c"),
        b.compile_source("../utils/blas/dgemv.c"),
    ],
    libraries="$(LIBS)",
)

analysis = simple_command(
    "python {0} analyze {out}",
    "analysis.json",
    ["main.py"],
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
    alias("build", [build]),
    Ruleset(macros={
        "CFLAGS": "-O3 -g",
        "CPPFLAGS": "-DNDEBUG -I../utils/blas",
        "LIBS": "-lm",
    }),
)

makefile.save()
