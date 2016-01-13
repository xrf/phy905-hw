#!/usr/bin/env python
import itertools, locale, logging, os, re, subprocess

PREFERREDENCODING = locale.getpreferredencoding(True)

def compile_c_exe(src_fn, exe_fn=None, macros={}, cc="cc", cflags=[]):
    exe_fn = exe_fn or os.path.splitext(src_fn)[0]
    macro_flags = (["-D", name + "=" + definition]
                   for name, definition in macros.items())
    macro_flags = list(itertools.chain(*macro_flags))
    args = [cc] + macro_flags + cflags + ["-o", exe_fn, src_fn]
    logging.info("Compiling {0} ...".format(src_fn))
    subprocess.check_call(args)

def first_word(string):
    return re.match("([\S]+)", string).group(1)

def parse_keyvalue_entry(line):
    key, value = line.split("=", 1)
    return key.strip(), value.strip()

def parse_keyvalues(string):
    lines = string.split("\n")
    return dict(parse_keyvalue_entry(line) for line in lines if line)

def suggested_num_repeats(mat_size):
    return 1 + int(NUM_REPEAT_PARAM / mat_size ** 3)

def suggested_max_test(mat_size, num_repeats):
    return 2 + int(MAX_TEST_PARAM / (mat_size ** 3 * num_repeats))

def bench(mat_size, num_repeats=None, max_test=None):
    num_repeats = num_repeats or suggested_num_repeats(mat_size)
    max_test = max_test or suggested_max_test(mat_size, num_repeats)
    macros = {
        "matSize": str(mat_size),
        "maxTest": str(max_test),
        "numRepeats": str(num_repeats),
    }
    logging.info("Benchmarking with mat_size = {0}, "
                 "max_test = {1}, num_repeats = {2} ..."
                 .format(mat_size, max_test, num_repeats))
    compile_c_exe("mmc.c", macros=macros, cc=CC, cflags=CFLAGS)
    output = subprocess.check_output(["./mmc"])
    output = parse_keyvalues(output.decode(PREFERREDENCODING))
    return {
        "time": float(first_word(output["Time"])),
        "rate": float(first_word(output["Rate"])),
    }

CFLAGS = ["-O2", "-mtune=native"]
CC = "clang"

# if your system is much faster than what I used, you may want to increase
# these parameters to increase accuracy at the cost of taking more time
NUM_REPEAT_PARAM = 1e8
MAX_TEST_PARAM = 1e9

logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

for mat_size in [100, 200, 400, 800, 1000, 1200, 1400, 1600, 2000]:
    result = bench(mat_size)
    print(mat_size, result["time"], result["rate"])
