#!/usr/bin/env python
import logging, sys
import matplotlib.pyplot as plt
import numpy as np
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

FIGSIZE = (6, 4.5)

@register_command(commands)
def bench(out_fn, *exes):
    import re
    data = [("size", "time_min", "time_mean", "time_stdev", "num_subrepeats")]
    for exe in exes:
        size = int(re.match(r".*?_(\d+)$", exe).group(1))
        logging.info("Benchmarking with SIZE = {0} ...".format(size))
        out = run_and_get_keyvalues([exe])
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
def analyze(fig_time_fn, fig_rate_fn, dummy_fn, data_fn):
    data = load_json_file(data_fn)
    size = np.array(data["size"])
    time = np.array(data["time_mean"])
    rate = 2 * 8 * size / time

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.loglog(size, time, "-x")
    ax.set_xlabel("array size (n)")
    ax.set_ylabel("time taken /s")
    fig.savefig(fig_time_fn, transparent=True)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_ylim(0, max(rate))
    ax.semilogx(data["size"], rate, "-x")
    ax.set_xlabel("array size (n)")
    ax.set_ylabel("rate /(MB/s)")
    fig.savefig(fig_rate_fn, transparent=True)

    save_file(dummy_fn, "")

def main_table():
    import json
    data = json.loads(read_file("data.json"))
    data["c1"] = "{:.3g}".format(data["c1"] * 1e9)
    data["c2"] = "{:.3g}".format(data["c2"] * 1e9)
    table = transpose(data["data"])
    table[1] = ["{:.0f}".format(x) for x in table[1]]
    table[3] = ["{:.3g}".format(x) for x in table[3]]
    table[4] = ["{:.3g}".format(x) for x in table[4]]
    data["data"] = table_to_html(transpose(table)).rstrip()
    write_file("index.html",
               main_template(substitute_template("template.html", data)))

def main():
    init_logging()
    run_command(commands)

if __name__ == "__main__":
    main()
