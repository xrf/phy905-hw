#!/usr/bin/env python
import itertools, json, locale, logging, os, re, subprocess
import matplotlib.pyplot as plt
import numpy as np

PREFERREDENCODING = locale.getpreferredencoding(True)

def first_word(string):
    return re.match("([\S]+)", string).group(1)

def parse_keyvalue_entry(line, sep):
    key, value = line.split(sep, 1)
    return key.strip(), value.strip()

def parse_keyvalues(string, sep):
    lines = string.split("\n")
    return dict(parse_keyvalue_entry(line, sep) for line in lines if line)

def parse_logging_level(level):
    if level is None:
        return
    level = str(level).upper()
    try:
        return int(level)
    except ValueError:
        pass
    lvl = getattr(logging, level, None)
    if isinstance(lvl, int):
        return lvl
    logging.warn("Invalid logging level: " + level)

def init_logging(level=None):
    config = {
        "format": "[%(levelname)s] %(message)s",
    }
    level = parse_logging_level(level or os.environ.get("LOGLEVEL", None))
    if level is not None:
        config["level"] = level
    logging.basicConfig(**config)

def compile_c_exe(src_fn, exe_fn=None, macros={}, cc="cc", cflags=[]):
    exe_fn = exe_fn or os.path.splitext(src_fn)[0]
    macro_flags = (["-D", name + "=" + definition]
                   for name, definition in macros.items())
    macro_flags = list(itertools.chain(*macro_flags))
    args = [cc] + macro_flags + cflags + ["-o", exe_fn, src_fn]
    logging.debug("Compiling {0} ...".format(args))
    subprocess.check_call(args)

CFLAGS = ["-O2", "-mtune=native"]
CC = "clang"

def suggested_num_repeats(mat_size, **params):
    return (params["num_repeats_offset"] + 1 +
            int(params["num_repeats_factor"] / mat_size ** 3))

def suggested_max_test(mat_size, num_repeats, **params):
    return (params["max_test_offset"] + 1 +
            int(params["max_test_factor"] / (mat_size ** 3 * num_repeats)))

def bench(mat_size, num_repeats=None, max_test=None, **params):
    num_repeats = num_repeats or suggested_num_repeats(mat_size, **params)
    max_test = max_test or suggested_max_test(mat_size, num_repeats, **params)
    macros = {
        "matSize": str(mat_size),
        "maxTest": str(max_test),
        "numRepeats": str(num_repeats),
    }
    logging.info("Benchmarking with matSize = {0}, "
                 "maxTest = {1}, numRepeats = {2} ..."
                 .format(mat_size, max_test, num_repeats))
    compile_c_exe("mmc.c", macros=macros, cc=CC, cflags=CFLAGS)
    output = subprocess.check_output(["./mmc"], universal_newlines=True)
    output = parse_keyvalues(output, sep="=")
    return {
        "time": float(first_word(output["Time"])),
        "rate": float(first_word(output["Rate"])),
    }

def get_max_clock_freq():
    output = subprocess.check_output(["lscpu"], universal_newlines=True)
    output = parse_keyvalues(output, sep=":")
    max_clock_freq = float(output["CPU max MHz"]) * 1e6
    logging.info("Maximum CPU frequency / MHz = {0}"
                 .format(max_clock_freq / 1e6))
    return max_clock_freq

def get_model_c(mat_size, time):
    return time / (2 * mat_size ** 3)

def model(mat_size, c):
    return 2 * c * mat_size ** 3

def run_bench(data_fn):
    if os.path.exists(data_fn):
        return

    mat_sizes = [100, 200, 400, 800, 1000, 1200, 1400, 1600, 2000]
    params = {}
    # if your system is much faster than what I used you may want to increase
    # these parameters a bit; doing so will increase timing accuracy at the
    # cost of taking more time
    bench_params = {
        # all parameters must be positive
        "num_repeats_offset": 3,
        "num_repeats_factor": 1e9,
        "max_test_offset": 3,
        "max_test_factor": 1e10,
    }
    logging.debug("benchmark parameters: {0}".format(bench_params))

    clock_freq = get_max_clock_freq()
    params["c2"] = 1. / clock_freq
    print("\t".join([
        "matSize",
        "rate",
        "time",
        "model1",
        "model2",
    ]))
    data = []
    for mat_size in mat_sizes:
        result = bench(mat_size, **bench_params)
        if mat_size == 100:
            params["c1"] = get_model_c(mat_size, result["time"])
        model_1_time = model(mat_size, params["c1"])
        model_2_time = model(mat_size, params["c2"])
        data.append([
            mat_size,
            result["rate"],
            result["time"],
            model_1_time,
            model_2_time,
        ])
        print("{0}\t{1:.2g}\t{2:.2g}\t{3:.2g}\t{4:.2g}".format(*data[-1]))
    print("")
    print("c1 = {0}".format(params["c1"]))
    print("c2 = {0}".format(params["c2"]))
    params["data"] = data
    with open(data_fn, "w") as f:
        json.dump(params, f)

def show_plot(data_fn):
    with open(data_fn, "r") as f:
        params = json.load(f)

    mat_size, rate, time, _, _ = zip(*params["data"])
    mat_size_range = np.linspace(min(mat_size), max(mat_size))
    model1 = model(mat_size_range, params["c1"])
    model2 = model(mat_size_range, params["c2"])

    ax = plt.subplots()[1]
    ax.set_ylim(0, max(rate))
    ax.semilogx(mat_size, rate, "-x")
    ax.set_xlabel("matrix size (N)")
    ax.set_ylabel("performance /MFLOPS")

    ax = plt.subplots()[1]
    ax.loglog(mat_size, time, "-x")
    ax.loglog(mat_size_range, model1)
    ax.loglog(mat_size_range, model2)
    ax.set_xlabel("matrix size (N)")
    ax.set_ylabel("time /s")

    plt.show()

def arg_parser(*args, **kwargs):
    import argparse
    p = argparse.ArgumentParser()

    p.add_argument("--data-file", required=True)

    return p

def main():
    args = arg_parser().parse_args()
    init_logging()

    run_bench(args.data_file)
    show_plot(args.data_file)

if __name__ == "__main__":
    main()
