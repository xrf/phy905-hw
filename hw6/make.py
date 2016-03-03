from makegen import *

NAME = "pcopy"

def make_all():
    return alias("all", [report()]).merge(
        simple_command("makegen {0}", "Makefile", ["make.py"], no_clean=True),
        Ruleset(macros={
            "CFLAGS": "-Wall -O3 -fopenmp",
            "LIBS": "-lm",
        }),
    )

def build():
    b = RelocatedBuilder(root="..")
    return b.build_program(
        NAME,
        [
            b.compile_source(NAME + ".c"),
            b.compile_source("../utils/utils.c"),
            b.compile_source("../utils/time.c"),
        ],
        libraries="$(LIBS)",
    )

def bench():
    return simple_command(
        "python main.py bench {out} {0}",
        "bench.json",
        [build()],
    )

def analysis():
    return simple_command(
        "python {0} analyze {out} {1}",
        "analysis.json",
        ["main.py", bench()],
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

make_all().save()
