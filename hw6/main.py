#!/usr/bin/env python
import logging, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

FIGSIZE = (5, 3.5)
NTS = [1, 2, 4] #, 6, 8, 10, 12, 14, 16]
SIZE = 65536 * 128

@register_command(commands)
def bench(out_fn, exe):
    data = {
        "nt": [],
        "time": [],
        "time_err": [],
    }
    for nt in NTS:
        logging.info("Benchmarking with NT = {0} ...".format(nt))
        env = dict(os.environ)
        env["OMP_NUM_THREADS"] = str(nt)
        env["SIZE"] = str(SIZE)
        out = run_and_get_keyvalues([exe], env=env)
        data["nt"].append(int(nt))
        data["time"].append(float(out["mean"]))
        data["time_err"].append(float(out["stdev"]))
    save_json_file(out_fn, data, json_args=JSON_ARGS)

@register_command(commands)
def analyze(out_fn, fn):
    data = load_json_file(fn)
    time = np.array(data["time"])
    time_err = np.array(data["time_err"])
    rate = SIZE * 8 / time
    rate_err = time_err / time * rate
    data["rate"] = rate.tolist()
    data["rate_err"] = rate_err.tolist()
    save_json_file(out_fn, data, json_args=JSON_ARGS)

@register_command(commands)
def plot(out_fn, data_fn):
    data = load_json_file(data_fn)
    plot_args = {
        "alpha": .8,
        "linewidth": 2,
        "markeredgecolor": "none",
    }
    fig_fns = {
        "fig_time_fn": "fig-time.svg",
        "fig_rate_fn": "fig-rate.svg",
    }

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.errorbar(
        data["nt"],
        np.array(data["time"]) * 1e3,
        yerr=np.array(data["time_err"]) * 1e3,
        color="#e91e63",
        **plot_args
    )
    ax.get_xaxis().set_major_locator(plt.MaxNLocator(integer=True))
    ax.set_xlabel("number of threads")
    ax.set_ylabel("time taken /ms")
    ax.grid("on")
    fig.tight_layout()
    fig.savefig(fig_fns["fig_time_fn"], transparent=True)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.errorbar(
        data["nt"],
        np.array(data["rate"]) / 1e6,
        yerr=np.array(data["rate_err"]) / 1e6,
        color="#4caf50",
        **plot_args
    )
    ax.get_xaxis().set_major_locator(plt.MaxNLocator(integer=True))
    ax.set_xlabel("number of threads")
    ax.set_ylabel("rate /(MB/s)")
    ax.grid("on")
    fig.tight_layout()
    fig.savefig(fig_fns["fig_rate_fn"], transparent=True)

    save_json_file(out_fn, fig_fns, json_args=JSON_ARGS)

@register_command(commands)
def report(out_fn, data_fn, figs_fn, template_fn):
    import cgi
    data = load_json_file(data_fn)
    table = [
        ["{0}".format(x) for x in data["nt"]],
        ["{0:.3g}".format(x) for x in data["time"]],
        ["{0:.3g}".format(x / 1e6) for x in data["rate"]],
    ]
    params = load_json_file(figs_fn)
    params["data"] = table_to_html(transpose(table)).rstrip()
    html = main_template(substitute_template(template_fn, params))
    save_file(out_fn, html)

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
