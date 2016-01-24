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

def guess_src_lang(ext):
    if ext.startswith("."):
        ext = ext[1:]
    if ext == "c":
        return "c"
    if ext in [".cc", ".cpp", ".cxx", ".c++"]:
        return "c++"
    return ext

def guess_compiler(lang):
    if lang == "c":
        return os.environ.get("CC", "cc")
    if lang == "c++":
        return os.environ.get("CXX", "c++")
    raise ValueError("Unknown lang: " + str(lang))

def guess_linker(lang=None):
    if lang:
        return guess_compiler(lang)
    return os.environ.get("LD", "ld")

def macros_to_flags(macros):
    return list(itertools.chain(*(
        ["-D", name + "=" + definition]
        for name, definition in macros.items()
    )))

def compile_src(*src_fns, out_fn=None, lang=None, link=False,
                macros={}, compiler=None, flags=[]):
    src_bn, src_ext = os.path.splitext(src_fns[0])
    lang = guess_src_lang(src_ext)
    if link:
        out_fn = out_fn or src_bn
    else:
        out_fn = out_fn or src_fns[0] + ".o"
        flags = ["-c"] + flags
    compiler = compiler or guess_compiler(lang=lang)
    flags = macros_to_flags(macros) + flags
    args = [compiler] + flags + ["-o", out_fn] + list(src_fns)
    logging.debug("Compiling {0} ...".format(args))
    subprocess.check_call(args)

def link_objs(lang, out_fn, *obj_fns, linker=None, flags=[]):
    linker = linker or guess_linker(lang=lang)
    args = [linker] + flags + ["-o", out_fn] + list(obj_fns)
    logging.debug("Linking {0} ...".format(args))
    subprocess.check_call(args)

CFLAGS = ["-O2", "-mtune=native"]

def suggested_num_repeats(mat_size, **params):
    return (params["num_repeats_offset"] + 1 +
            int(params["num_repeats_factor"] / mat_size ** 3))

def suggested_max_test(mat_size, num_repeats, **params):
    return (params["max_test_offset"] + 1 +
            int(params["max_test_factor"] / (mat_size ** 3 * num_repeats)))

def build(macros):
    compile_src("dummy.c", flags=CFLAGS)
    compile_src("mysecond.c", flags=CFLAGS)
    compile_src("mmc.c", macros=macros, flags=CFLAGS)
    link_objs("c", "mmc", "mmc.c.o", "dummy.c.o", "mysecond.c")

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
    build(macros)
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

def run_bench(data_fn, **kwargs):
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

def show_plot(data_fn, fig_time_fn, fig_perf_fn, quiet=False, **kwargs):
    with open(data_fn, "r") as f:
        params = json.load(f)

    mat_size, rate, time, _, _ = zip(*params["data"])
    mat_size_range = np.linspace(min(mat_size), max(mat_size))
    model1 = model(mat_size_range, params["c1"])
    model2 = model(mat_size_range, params["c2"])

    figsize = (6, 4.5)

    fig, ax = plt.subplots(figsize=figsize)
    ax.set_ylim(0, max(rate))
    ax.semilogx(mat_size, rate, "-x")
    ax.set_xlabel("matrix size (N)")
    ax.set_ylabel("performance /MFLOPS")
    if fig_perf_fn is not None:
        fig.savefig(fig_perf_fn, transparent=True)

    fig, ax = plt.subplots(figsize=figsize)
    ax.loglog(mat_size, time, "-x", label="measured")
    ax.loglog(mat_size_range, model1, label="model #1")
    ax.loglog(mat_size_range, model2, label="model #2")
    ax.set_xlabel("matrix size (N)")
    ax.set_ylabel("time /s")
    ax.legend(loc=4)
    if fig_time_fn is not None:
        fig.savefig(fig_time_fn, transparent=True)

    if not quiet:
        plt.show()

def arg_parser(*args, **kwargs):
    import argparse
    p = argparse.ArgumentParser()

    p.add_argument(
        "--data",
        dest="data_fn",
        metavar="FILE",
        required=True,
        help="where to write/read the data file",
    )
    p.add_argument(
        "--fig-time",
        dest="fig_time_fn",
        metavar="FILE",
        help="where to save the figure",
    )
    p.add_argument(
        "--fig-perf",
        dest="fig_perf_fn",
        metavar="FILE",
        help="where to save the figure",
    )
    p.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="don't display figures",
    )

    return p

def main():
    args = vars(arg_parser().parse_args())
    init_logging()
    run_bench(**args)
    show_plot(**args)

if __name__ == "__main__":
    main()
