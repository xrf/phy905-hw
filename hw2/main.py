#!/usr/bin/env python
import logging, sys
import matplotlib.pyplot as plt
import numpy as np
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

FIGSIZE = (6, 4)

@register_command(commands)
def bench(out_fn, *copy_exes):
    import re
    data = [("size", "time_min", "time_mean", "time_stdev", "num_subrepeats")]
    for copy_exe in copy_exes:
        size = int(re.match(r".*?_(\d+)$", copy_exe).group(1))
        logging.info("Benchmarking with SIZE = {0} ...".format(size))
        out = run_and_get_keyvalues([copy_exe])
        data.append((
            size,
            float(out["min"]),
            float(out["mean"]),
            float(out["stdev"]),
            int(out["num_subrepeats"]),
        ))
    data = tablerows_to_tablecols(data)
    save_json_file(out_fn, data)

@register_command(commands)
def plot(dummy_fn, data_fn):
    fig_time_fn = "fig-time.svg"
    fig_rate_fn = "fig-rate.svg"

    data = load_json_file(data_fn)
    size = np.array(data["size"])
    time = np.array(data["time_mean"])
    rate = 2 * 8 * size / time / 1e6

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.loglog(size, time, "-x")
    ax.set_xlabel("array size (n)")
    ax.set_ylabel("time taken /s")
    fig.tight_layout()
    fig.savefig(fig_time_fn, transparent=True)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.semilogx(data["size"], rate, "-x")
    ax.set_xlabel("array size (n)")
    ax.set_ylabel("rate /(MB/s)")
    fig.tight_layout()
    fig.savefig(fig_rate_fn, transparent=True)

    save_file(dummy_fn, "")

@register_command(commands)
def analyze(out_fn, data_fn, report_fn, template_fn):
    import cgi

    data = load_json_file(data_fn)
    size = np.array(data["size"])
    time = np.array(data["time_mean"])
    rate = 2 * 8 * size / time / 1e6

    table = [
        ["{0}".format(x) for x in size],
        ["{0:.3g}".format(x) for x in time],
        ["{0:.3g}".format(x) for x in rate],
    ]
    data["code"] = cgi.escape(load_file("copy.c"))
    data["data"] = table_to_html(transpose(table)).rstrip()
    data["report"] = cgi.escape(load_file(report_fn))
    html = main_template(substitute_template(template_fn, data))
    save_file(out_fn, html)

def main():
    init_logging()
    run_command(commands)

if __name__ == "__main__":
    main()
