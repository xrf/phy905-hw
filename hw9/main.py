#!/usr/bin/env python
import glob, json, logging, os, re, subprocess, sys
import numpy as np
import pandas as pd
import matplotlib
#matplotlib.use("Agg")
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
    sort_dataframe(data, "size")

    time = data["time_min"]
    fit = [
        np.linalg.lstsq(np.array(data["size"])[:, np.newaxis], time)[0][0],
        0
    ]

    fig_fit_fn = "fig-fit.svg"
    fig, ax = plt.subplots()
    ax.plot(data["size"], time, label="data", marker="x", linestyle="")
    ax.plot(data["size"], np.poly1d(fit)(data["size"]), label="fit")
    ax.set_xlabel("number of double-precision floating-point elements")
    ax.set_ylabel("time taken to transfer to another process and back /s")
    ax.grid("on")
    legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    fig.savefig(fig_fit_fn,
                bbox_extra_artists=(legend,),
                bbox_inches="tight",
                transparent=True)

    # the factor of two accounts for the fact that we are sending data and
    # receiving it again
    bandwidth = 2 * 8. / fit[0]
    json.dump({
        "data": data,
        "fig_fit_fn": fig_fit_fn,
        "fit": fit,
        "bandwidth /(B/s)": bandwidth,
    }, sys.stdout, **JSON_ARGS)
    sys.stdout.write("\n")

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
    sort_dataframe(data, "method")
    sort_dataframe(data, "np")
    sort_dataframe(data, "size")

    records = dataframe_to_records(data)
    groups = group_records_by(records, ["size", "method"])
    grouped_data = {}
    for key, group in sorted(groups.items()):
        size, method = key
        series = {
            "color": {
                102400: "#e91e63",
                16384: "#f29312",
                1024: "#4caf50",
            }[size],
            "linestyle": {
                "allgather": "-",
                "circulate": "--",
            }[method],
            "label": "M={0},{1}".format(size, method),
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

    mpi_rate = 1.5e9
    flops = 4e9
    mem_rate = 5e9
    def model(N, m):
        return (
            2. * m * (1. - 1. / N) * 8. / mpi_rate +
            2. * m ** 2 / N * (1. / flops + 8. / mem_rate)
        )

    fig, ax = plt.subplots(figsize=figsize)
    prev_series = None
    for _, series in sorted(grouped_data.items()):
        series = pd.DataFrame.from_dict(series)
        if prev_series is None or series["size"][0] != prev_series["size"][0]:
            prev_series = series
            if prev_series is not None:
                N = np.linspace(min(prev_series["np"]), max(prev_series["np"]))
                size = prev_series["size"][0]
                ax.plot(
                    N,
                    model(N=N, m=size),
                    label="M={0},fit".format(size),
                    color=prev_series["color"][0],
                    linestyle=":",
                    **plot_args)
        ax.plot(
            series["np"],
            series[TIME],
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
def report(out_fn, data_fn, figs_fn, index_fn):
    template_fn = ".template.html.tmp"
    datafile = load_json_file(data_fn)
    data = load_json_file(data_fn)["data"]
    subprocess.check_call(["pandoc", "-f", "commonmark",
                           "-t", "html", "-o", template_fn, index_fn])
    table = [
        [str(x) for x in data["method"]],
        [str(x) for x in data["np"]],
        [str(x) for x in data["size"]],
        ["{0:.3g}".format(x) for x in data[TIME]],
    ]
    params = load_json_file(figs_fn)
    params["data"] = table_to_html(transpose(table)).rstrip()
    html = main_template(substitute_template(template_fn, params))
    html = html.replace("^2", "<sup>2</sup>")
    save_file(out_fn, html)

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
