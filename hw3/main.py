#!/usr/bin/env python
import logging, sys
import matplotlib.pyplot as plt
import numpy as np
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

FIGSIZE = (6, 4)

@register_command(commands)
def bench(out_fn, *exes):
    import re
    data = [("bsize", "size", "time_min", "time_mean",
             "time_stdev", "num_subrepeats")]
    for exe in exes:
        bsize, size = re.match(r".*?_(\d+)_(\d+)$", exe).groups()
        bsize = int(bsize)
        size = int(size)
        logging.info("Benchmarking transpose with BSIZE = {0}, SIZE = {1} ..."
                     .format(bsize, size))
        out = run_and_get_keyvalues([exe])
        data.append((
            bsize,
            size,
            float(out["min"]),
            float(out["mean"]),
            float(out["stdev"]),
            int(out["num_subrepeats"]),
        ))
    data = tablerows_to_tablecols(data)
    save_json_file(out_fn, data)

@register_command(commands)
def bench_co(out_fn, data_fn, exe):
    import subprocess
    data = load_json_file(data_fn)
    sizes = sorted(set(data["size"]))
    co_data = []
    for size in sizes:
        logging.info("Benchmarking cotranspose with SIZE = {0} ..."
                     .format(size))
        out = subprocess.check_output([exe, str(size)],
                                      universal_newlines=True)
        out = "\n".join(out.split("\n")[1:])
        out = parse_keyvalues(out, sep="=")
        co_data.append(float(out["Time"]))
    save_json_file(out_fn, co_data)

@register_command(commands)
def analyze(out_fn, data_fn, co_data_fn):
    data = load_json_file(data_fn)
    sizes = np.array(sorted(set(data["size"])))
    time_basic = [x[1] for x in
                  sorted([(size, time)
                          for size, time, bsize in
                          zip(data["size"], data["time_mean"], data["bsize"])
                          if bsize < 2])]
    time_model = 16 * sizes * sizes / 6770. * 1e-6
    time_blocked = [x[1] for x in
                    sorted([(size, time)
                            for size, time, bsize in
                            zip(data["size"], data["time_mean"], data["bsize"])
                            if bsize >= 2])]
    time_co = load_json_file(co_data_fn)
    save_json_file(out_fn, {
        "size": list(map(int, sizes)),
        "time_basic": time_basic,
        "time_model": list(map(float, time_model)),
        "time_blocked": time_blocked,
        "time_co": time_co,
    })

@register_command(commands)
def plot(fig_time_fn, data_fn):
    fig_time_fn = "fig-time.svg"
    fig_compare_fn = "fig-compare.svg"
    data = load_json_file(data_fn)
    size = data["size"]
    time_basic = np.array(data["time_basic"])
    time_model = np.array(data["time_model"])
    time_blocked = np.array(data["time_blocked"])
    time_co = np.array(data["time_co"])

    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot = ax.loglog
    plot(size, time_basic, "-x", label="basic")
    plot(size, time_model, "-x", label="model")
    plot(size, time_blocked, "-x", label="blocked")
    plot(size, time_co, "-x", label="cache-oblivious")
    ax.set_xlabel("matrix size (n)")
    ax.set_ylabel("time taken /s")
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(fig_time_fn, transparent=True)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot = ax.semilogx
    plot(size, time_basic / time_model, "-x", label="basic")
    plot(size, time_blocked / time_model, "-x", label="blocked")
    plot(size, time_co / time_model, "-x", label="cache-oblivious")
    ax.set_xlabel("matrix size (n)")
    ax.set_ylabel("ratio of time taken to model time")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(fig_compare_fn, transparent=True)

@register_command(commands)
def tabulate(out_fn, data_fn, fig_time_fn, template_fn):
    import cgi
    fig_compare_fn = "fig-compare.svg"
    data = load_json_file(data_fn)
    table = [
        ["{0}".format(x) for x in data["size"]],
        ["{0:.3g}".format(x * 1e6) for x in data["time_basic"]],
        ["{0:.3g}".format(x * 1e6) for x in data["time_model"]],
        ["{0:.3g}".format(x * 1e6) for x in data["time_blocked"]],
        ["{0:.3g}".format(x * 1e6) for x in data["time_co"]],
    ]
    data["data"] = table_to_html(transpose(table)).rstrip()
    data["fig_time_fn"] = fig_time_fn
    data["fig_compare_fn"] = fig_compare_fn
    html = main_template(substitute_template(template_fn, data))
    save_file(out_fn, html)

def main():
    init_logging()
    run_command(commands)

if __name__ == "__main__":
    main()
