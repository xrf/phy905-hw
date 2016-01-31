import functools
from makegen import *
import params

b = RelocatedBuilder(root="..")

build_copy = [b.build_program("hw2_copy_{0}".format(size), [
    b.compile_source("copy.c", macros={
        "SIZE": str(size),
        "REPEATS": str(8),
    }, suffix="_{0}".format(size)),
    b.compile_source("../utils/utils.c"),
    b.compile_source("../utils/time.c"),
], libraries=[Library("m")]) for size in params.SIZES]

bench = simple_command("./main.py bench", "data.json", build_copy)

analyze = simple_command("./main.py analyze fig-time.svg fig-rate.svg",
                         "../dist/tmp/analyze.ok", [bench])

stream = b.build_program("stream", [
    b.compile_source("../ext/stream.c", macros={
        "STREAM_ARRAY_SIZE": "$(STREAM_ARRAY_SIZE)"
    }),
]).merge(Ruleset(macros={"STREAM_ARRAY_SIZE": str(2 ** 24)}))

alias("all", (
    [
        stream,
        analyze
    ]
)).merge(Ruleset(macros={
    "CFLAGS": "-O2 -mtune=native"
})).save()
