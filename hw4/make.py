from makegen import *

NAME = "multiply"
SIZES = [20, 40, 60, 80, 100, 150, 200, 300, 400, 600, 800, 1000]
BSIZES = [1, 128]
OPTLEVELS = [0, 1, 2, 3]

def make_all():
    return alias("all", [report()]).merge(
        simple_command("makegen {0}", "Makefile", ["make.py"]),
        Ruleset(macros={
            "CFLAGS": "-Wall -O3",
        }),
    )

def benchs():
    return [
        bench_program(
            suffix="_{0:03}_{1:04}_{2}".format(bsize, size, optlevel),
            macros={
                "BSIZE": str(bsize),
                "SIZE": str(size),
            },
            extra_flags=["-O{0}".format(optlevel)],
        )
        for bsize in BSIZES
        for size in SIZES
        for optlevel in OPTLEVELS
    ]

def data():
    return simple_command(
        "python {0} merge {out} {all1}",
        "data.json",
        ["main.py"] + benchs(),
    )

def plot():
    return simple_command(
        "python {0} plot {out} {all1}",
        "figs.json",
        ["main.py", data()],
    )

def report():
    return simple_command(
        "python {0} report {out} {all1}",
        "index.html",
        ["main.py", data(), plot(), "template.html"],
    )

def bench_program(suffix=None, macros={}, extra_flags={}):
    import os
    prefix = os.path.basename(os.path.dirname(os.path.abspath(__file__))) + "_"
    b = RelocatedBuilder(root="..")
    build = b.build_program(
        "{0}{1}{2}".format(prefix, NAME, suffix or ""),
        [
            b.compile_source(
                NAME + ".c",
                macros=macros,
                suffix=suffix,
                extra_flags=extra_flags,
            ),
            b.compile_source("../utils/utils.c"),
            b.compile_source("../utils/time.c"),
        ],
        libraries=[Library("m")],
    )
    bench = simple_command(
        "python main.py bench {out} {0}",
        "data{0}.json".format(suffix or ""),
        [build],
    )
    return bench

make_all().save()
