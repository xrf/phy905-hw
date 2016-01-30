from makegen import *

def build_copy(**kwargs):
    macros = dict((k.upper(), str(v)) for k, v in kwargs.items())
    return build_program("dist/copy_" + hash_json(kwargs), [
        compile_source("copy.c", macros=macros),
        compile_source("../utils/time.c"),
        compile_source("../utils/utils.c"),
    ], libraries="m")

save_makefile("Makefile", alias("all", [
    build_copy(size=size, repeats=8)
    for size in [100, 1000, 10000]
]).emit())
