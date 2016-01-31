import functools
from makegen import *
import params

b = RelocatedBuilder(root="..")

build_copy = [b.build_program("hw2_copy_{0:07}".format(size), [
    b.compile_source("copy.c", macros={
        "SIZE": str(size),
        "REPEATS": str(8),
    }, suffix="_{0:07}".format(size)),
    b.compile_source("../utils/utils.c"),
    b.compile_source("../utils/time.c"),
], libraries=[Library("m")]) for size in params.SIZES]

bench = simple_command("./main.py bench {out} {all}", "data.json", build_copy)

stream = b.build_program("stream", [
    b.compile_source("../ext/stream.c", macros={
        "STREAM_ARRAY_SIZE": "$(STREAM_ARRAY_SIZE)"
    }),
]).merge(Ruleset(macros={"STREAM_ARRAY_SIZE": str(2 ** 24)}))

report = simple_command("{0} >{out}.tmp && mv {out}.tmp {out}",
                        "report.txt", [stream])

plot = simple_command("./main.py plot {out} {all}",
                      "../dist/tmp/hw2/plot.ok", [bench])

analyze = simple_command("./main.py analyze {out} {all}",
                         "index.html", [bench, report, "template.html"])

alias("all", [analyze, plot]).merge(Ruleset(macros={
    "CFLAGS": "-O2 -mtune=native"
})).save()
