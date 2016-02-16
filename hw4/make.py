from makegen import *

NAME = "multiply"
SIZES = [20, 40, 60, 80, 100, 150, 200, 300, 400, 600, 800, 1000]
BSIZES = [1, 128]
OPTLEVELS = [0, 1, 2, 3]

def make_all():
    return alias("all", [report()]).merge(
        simple_command("makegen {0}", "Makefile", ["make.py"], no_clean=True),
        Ruleset(macros={
            "CFLAGS": "-Wall -O3",
            "LIBS": "-lm",
        }),
    )

def benchs():
    return compile_before_benching(
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
    )

def data():
    return simple_command(
        "python {0} merge {out} {all1}",
        "data.json",
        ["main.py"] + benchs(),
    )

def analysis():
    return simple_command(
        "python {0} analyze {out} {all1}",
        "analysis.json",
        ["main.py", data()],
    )

def plot():
    return simple_command(
        "python {0} plot {out} {all1}",
        "figs.json",
        ["main.py", analysis()],
    )

def report():
    return simple_command(
        "python {0} report {out} {all1}",
        "index.html",
        ["main.py", analysis(), plot(), "template.html"],
    )

def prefix(name):
    import os
    return "{0}_{1}".format(
        os.path.basename(os.path.dirname(os.path.abspath(__file__))),
        name,
    )

def bench_program(suffix=None, macros={}, extra_flags={}):
    b = RelocatedBuilder(root="..")
    build = b.build_program(
        "{0}{1}".format(prefix(NAME), suffix or ""),
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
        libraries="$(LIBS)",
    )
    def bench(buildall):
        return simple_command(
            "python main.py bench {out} {0}",
            "../dist/tmp/{0}{1}.json".format(prefix(NAME), suffix or ""),
            [build, buildall],
        )
    return build, bench

def compile_before_benching(build_bench_list):
    '''Make sure everything is compiled before starting the benchmarks.'''
    build_bench_list = tuple(build_bench_list)
    builds = [build for build, _ in build_bench_list]
    # .PHONY overrides .SECONDARY so we need an extra indirection
    buildall = simple_command(
        "touch {out}",
        "../dist/tmp/{0}_build.ok".format(prefix(NAME)),
        builds,
    )
    buildall = buildall.merge(alias("build", [buildall]))
    return [bench(buildall) for _, bench in build_bench_list]

make_all().save()
