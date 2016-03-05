#!/usr/bin/env python
import logging, os, subprocess, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

ERR = False
SIZES = [20, 40, 60, 80, 100, 150, 200, 300, 400, 600, 800, 1000]

@register_command(commands)
def bench(out_fn, exe, exe_omp):
    data = {
        "nt": [],
        "size": [],
        "time": [],
        "time_err": [],
    }
    num_cores = get_num_cores()
    for size in SIZES:
        logging.info("Benchmarking with SIZE = {0} (no OpenMP) ..."
                     .format(size))
        env = dict(os.environ)
        env["SIZE"] = str(size)
        out = run_and_get_keyvalues([exe], env=env)
        data["nt"].append(0)
        data["size"].append(size)
        data["time"].append(float(out["mean"]))
        data["time_err"].append(float(out["stdev"]))
    for nt in range(1, num_cores + 1):
        for size in SIZES:
            logging.info("Benchmarking with NT = {0}, SIZE = {1} ..."
                         .format(nt, size))
            env = dict(os.environ)
            env["OMP_NUM_THREADS"] = str(nt)
            env["SIZE"] = str(size)
            out = run_and_get_keyvalues([exe_omp], env=env)
            data["nt"].append(nt)
            data["size"].append(size)
            data["time"].append(float(out["mean"]))
            data["time_err"].append(float(out["stdev"]))
    save_json_file(out_fn, data, json_args=JSON_ARGS)

@register_command(commands)
def analyze(out_fn, fn):
    data = load_json_file(fn)

    size = np.array(data["size"])
    time = np.array(data["time"])
    time_err = np.array(data["time_err"])
    rate = 2 * size ** 3 / time
    rate_err = 3 * time_err / time * rate
    data["rate"] = rate.tolist()
    data["rate_err"] = rate_err.tolist()

    records = dataframe_to_records(data)
    groups = group_records_by(records, ["nt"])
    grouped_data = []
    for (nt,), group in sorted(groups.items()):
        series = {
            "color": {
                0: "#222222",
                1: "#e91e63",
                2: "#f29312",
                3: "#4caf50",
                4: "#2196f3",
            }[nt],
            "linestyle": "-" if nt else "--",
            "label": ("OpenMP with {0} threads".format(nt)
                     if nt else "No OpenMP"),
        }
        series.update(records_to_dataframe(group))
        grouped_data.append(series)

    save_json_file(out_fn, {
        "data": data,
        "grouped_data": grouped_data,
    }, json_args=JSON_ARGS)

def plot_args(yerr=None):
    kwargs = {
        "alpha": .8,
        "linewidth": 2,
        "markeredgecolor": "none",
    }
    if ERR and yerr is not None:
        kwargs["yerr"] = yerr
    return kwargs

@register_command(commands)
def plot(out_fn, data_fn):
    data = load_json_file(data_fn)["grouped_data"]
    figsize = (5, 3.5)
    fig_fns = {
        "fig_time_fn": "fig-time.svg",
        "fig_rate_fn": "fig-rate.svg",
    }

    fig, ax = plt.subplots(figsize=figsize)
    for series in data:
        ax.errorbar(
            series["size"],
            series["time"],
            label=series["label"],
            color=series["color"],
            linestyle=series["linestyle"],
            **plot_args(yerr=series["time_err"]))
    ax.get_xaxis().set_major_locator(plt.MaxNLocator(integer=True))
    ax.set_xlabel("matrix size")
    ax.set_ylabel("time taken /s")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid("on")
    fig.tight_layout()
    fig.savefig(fig_fns["fig_time_fn"], transparent=True)
    legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    fig.savefig(fig_fns["fig_time_fn"],
                bbox_extra_artists=(legend,),
                bbox_inches="tight",
                transparent=True)

    fig, ax = plt.subplots(figsize=figsize)
    for series in data:
        ax.errorbar(
            series["size"],
            np.array(series["rate"]) / 1e9,
            label=series["label"],
            color=series["color"],
            linestyle=series["linestyle"],
            **plot_args(yerr=np.array(series["rate_err"]) / 1e9))
    ax.get_xaxis().set_major_locator(plt.MaxNLocator(integer=True))
    ax.set_xlabel("matrix size")
    ax.set_ylabel("performance /GFLOPS")
    ax.set_xscale("log")
    ax.grid("on")
    fig.tight_layout()
    fig.savefig(fig_fns["fig_rate_fn"], transparent=True)
    legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    fig.savefig(fig_fns["fig_rate_fn"],
                bbox_extra_artists=(legend,),
                bbox_inches="tight",
                transparent=True)

    save_json_file(out_fn, fig_fns, json_args=JSON_ARGS)

@register_command(commands)
def report(out_fn, data_fn, figs_fn, template_fn):
    import cgi
    data = load_json_file(data_fn)["data"]
    table = [
        [str(x) if x else "(no OpenMP)" for x in data["nt"]],
        [str(x) for x in data["size"]],
        ["{0:.3g}".format(x) for x in data["time"]],
        ["{0:.3g}".format(x / 1e9) for x in data["rate"]],
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
