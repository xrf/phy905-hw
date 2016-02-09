import functools
from makegen import *

SIZES = [20, 100, 500, 800, 1000, 1500, 2000, 4000]
BSIZES = [1, 16]

b = RelocatedBuilder(root="..")

def render_suffix(bsize, size):
    return "_{0:02}_{1:07}".format(bsize, size)

build_transpose = [
    b.build_program(
        "hw3_transpose" + render_suffix(bsize, size),
        [
            b.compile_source(
                "transpose.c", macros={
                    "BSIZE": str(bsize),
                    "SIZE": str(size),
                },
                suffix=render_suffix(bsize, size),
                inherit_flags=False,
                extra_flags=["-O0"],
            ),
            b.compile_source("../utils/utils.c"),
            b.compile_source("../utils/time.c"),
        ],
        libraries=[Library("m")],
    )
    for bsize in BSIZES
    for size in SIZES
]

build_cotranspose = b.build_program(
    "hw3_cotranspose",
    [
        b.compile_source(
            "../ext/cotranspose.c",
            suffix="",
            inherit_flags=False,
            extra_flags=["-O0"],
        ),
    ],
)

bench = simple_command(
    "./main.py bench {out} {all}",
    "data.json",
    build_transpose,
)

bench_co = simple_command(
    "./main.py bench_co {out} {all}",
    "data_co.json",
    [bench, build_cotranspose],
)

analyze = simple_command(
    "./main.py analyze {out} {all}",
    "analysis.json",
    [bench, bench_co],
)

plot = simple_command(
    "./main.py plot {out} {all}",
    "fig-time.svg",
    [analyze],
)

tabulate = simple_command(
    "./main.py tabulate {out} {all}",
    "index.html",
    [analyze, plot, "template.html"],
)

alias("all", [tabulate]).merge(Ruleset(macros={
    "CFLAGS": "-O2"
})).save()
