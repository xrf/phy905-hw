#!/usr/bin/env python
import glob, logging, os, re, subprocess, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

TIME = "time_min"

@register_command(commands)
def estimate_bandwidth():
    data = {
        "size": [],
        "time_min": [],
        "time_mean": [],
        "time_stdev": [],
        "num_subrepeats": [],
    }
    for data_fn in sorted(glob.glob("bench_bandwidth/*.txt")):
        entries = parse_keyvalues(load_file(data_fn), "=")
        pattern = r"bench_bandwidth/(\d+).txt"
        size, = re.match(pattern, data_fn).groups()
        data["size"].append(int(size))
        data["time_min"].append(float(entries["min"]))
        data["time_mean"].append(float(entries["mean"]))
        data["time_stdev"].append(float(entries["stdev"]))
        data["num_subrepeats"].append(float(entries["num_subrepeats"]))
    fit = np.polyfit(data["size"], data["time_min"], 1)
    save_json_file(out_fn, {
        "data": data,
        "fit": fit.tolist(),
    }, json_args=JSON_ARGS)

@register_command(commands)
def analyze(out_fn):
    data = {
        "np": [],
        "method": [],
        "size": [],
        "time_min": [],
        "time_mean": [],
        "time_stdev": [],
        "num_subrepeats": [],
    }
    for data_fn in sorted(glob.glob("bench/*.txt")):
        entries = parse_keyvalues(load_file(data_fn), "=")
        pattern = r"bench/(\d+)_(\d+)_(\d+).txt"
        np, method, size = re.match(pattern, data_fn).groups()
        data["np"].append(int(np))
        data["method"].append([
            "allgather",
            "circulate",
        ][int(method) - 1])
        data["size"].append(int(size))
        data["time_min"].append(float(entries["min"]))
        data["time_mean"].append(float(entries["mean"]))
        data["time_stdev"].append(float(entries["stdev"]))
        data["num_subrepeats"].append(float(entries["num_subrepeats"]))

    records = dataframe_to_records(data)
    groups = group_records_by(records, ["size", "method"])
    grouped_data = {}
    for key, group in sorted(groups.items()):
        size, method = key
        series = {
            # "color": {
            #     128: "#e91e63",
            #     256: "#f29312",
            #     512: "#4caf50",
            #     1024: "#0caff0",
            # }[np],
            "color": {
                102400: "#e91e63",
                16384: "#f29312",
                1024: "#4caf50",
            }[size],
            "linestyle": {
                "allgather": "-",
                "circulate": "--",
            }[method],
            "label": "size={0},method={1}".format(size, method),
        }
        sort_key = lambda x: x["np"]
        series.update(records_to_dataframe(sorted(group, key=sort_key)))
        grouped_data[key] = series

    save_json_file(out_fn, {
        "data": data,
        "grouped_data": tuple(grouped_data.items()),
    }, json_args=JSON_ARGS)

@register_command(commands)
def plot(out_fn, data_fn):
    plot_args = {
        "alpha": .8,
        "linewidth": 2,
        "markeredgecolor": "none",
    }
    data = load_json_file(data_fn)
    grouped_data = dict((tuple(k), v) for k, v in data["grouped_data"])
    figsize = (5, 3.5)
    fig_fns = {
        "fig_time_fn": "fig-time.svg",
    }

    fig, ax = plt.subplots(figsize=figsize)
    for _, series in sorted(grouped_data.items()):
        series = pd.DataFrame.from_dict(series)
        ax.plot(
            series["np"],
            series[TIME], # / (series["size"] ** 2 / series["np"]),
            label=series["label"][0],
            color=series["color"][0],
            linestyle=series["linestyle"][0],
            **plot_args)
    ax.set_xlabel("number of processes")
    ax.set_ylabel("time taken /s")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(100, 1200)
    ax.grid("on")
    legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    fig.savefig(fig_fns["fig_time_fn"],
                bbox_extra_artists=(legend,),
                bbox_inches="tight",
                transparent=True)

    save_json_file(out_fn, fig_fns, json_args=JSON_ARGS)

@register_command(commands)
def report(out_fn, data_fn, figs_fn, template_fn):
    import cgi
    datafile = load_json_file(data_fn)
    data = load_json_file(data_fn)["data"]
    table = [
        [str(x) for x in data["case"]],
        [str(x) for x in data["test"]],
        [str(x) for x in data["size"]],
        ["{0:.3g}".format(x) for x in data["time"]],
    ]
    params = load_json_file(figs_fn)
    params["code"] = cgi.escape(load_file("mpicomm.c"))
    params["data"] = table_to_html(transpose(table)).rstrip()
    for i, cutoff in enumerate(datafile["cutoffs"]):
        params["cutoff_{0}".format(i)] = cutoff
    for i, fit in enumerate(datafile["fits"]):
        for j, p in enumerate(fit):
            params["fit_{0}_{1}".format(i, j)] = "{0:.3g}".format(p)
    html = main_template(substitute_template(template_fn, params))
    save_file(out_fn, html)

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
