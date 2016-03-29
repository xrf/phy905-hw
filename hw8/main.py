#!/usr/bin/env python
import logging, os, re, subprocess, sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

@register_command(commands)
def analyze(out_fn, *data_fns):
    data = {
        "test": [],
        "case": [],
        "size": [],
        "time": [],
    }
    for data_fn in data_fns:
        entries = parse_keyvalues(load_file(data_fn), "=")
        case, size = re.match(r"bench_(\d+)_(\d+).txt", data_fn).groups()
        data["test"].extend(["1a", "1b", "2a"])
        data["case"].extend([int(case)] * 3)
        data["size"].extend([int(size)] * 3)
        data["time"].extend([
            float(entries["time_1a /s"]),
            float(entries["time_1b /s"]),
            float(entries["time_2a /s"]),
        ])

    records = dataframe_to_records(data)
    groups = group_records_by(records, ["test", "case"])
    grouped_data = {}
    for (test, case), group in sorted(groups.items()):
        series = {
            "color": {
                1: "#e91e63",
                2: "#f29312",
                3: "#4caf50",
            }[case],
            "linestyle": {
                "1a": "-",
                "1b": "--",
                "2a": ":",
            }[test],
            "label": "case={1},test={0}".format(test, case),
        }
        series.update(records_to_dataframe(group))
        grouped_data[(test, case)] = series

    fitted_data_test_case = ("1a", 1)
    series = grouped_data[fitted_data_test_case]
    cutoffs = [1, 100, 10000, max(series["size"])]
    series = pd.DataFrame.from_dict(series)
    subseriess = [
        series[(series["size"] >= cutoffs[0]) & (series["size"] < cutoffs[1])],
        series[(series["size"] >= cutoffs[1]) & (series["size"] < cutoffs[2])],
        series[series["size"] >= cutoffs[2]],
    ]
    fits = [np.polyfit(subseries["size"], subseries["time"], 1)
            for subseries in subseriess]

    save_json_file(out_fn, {
        "data": data,
        "grouped_data": tuple(grouped_data.items()),
        "fitted_data_test_case": fitted_data_test_case,
        "cutoffs": cutoffs,
        "fits": [fit.tolist() for fit in fits],
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
        "fig_time_zoomed_fn": "fig-time-zoomed.svg",
        "fig_fit_0_fn": "fig-fit-0.svg",
        "fig_fit_1_fn": "fig-fit-1.svg",
        "fig_fit_2_fn": "fig-fit-2.svg",
    }
    ZOOMED_SIZE_MAX = 32

    for zoomed in ["", "_zoomed"]:
        fig, ax = plt.subplots(figsize=figsize)
        for _, series in sorted(grouped_data.items()):
            series = pd.DataFrame.from_dict(series)
            if zoomed:
                series = series[series["size"] <= ZOOMED_SIZE_MAX]
                series["time"] = series["time"] * 1e6
            ax.plot(
                series["size"],
                series["time"],
                label=series["label"][0],
                color=series["color"][0],
                linestyle=series["linestyle"][0],
                **plot_args)
        ax.set_xlabel("array size /B")
        if zoomed:
            ax.set_ylabel("time taken /us")
            ax.set_xlim(0, ZOOMED_SIZE_MAX)
        else:
            ax.set_ylabel("time taken /s")
            ax.set_xscale("log")
            ax.set_yscale("log")
        ax.grid("on")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        fig.savefig(fig_fns["fig_time{0}_fn".format(zoomed)],
                    bbox_extra_artists=(legend,),
                    bbox_inches="tight",
                    transparent=True)

    series = pd.DataFrame.from_dict(grouped_data[("1a", 1)])
    cutoffs = [min(series["size"]), 100, 10000, max(series["size"])]
    subseriess = [
        series[series["size"] <= cutoffs[1]],
        series[(series["size"] > cutoffs[1]) & (series["size"] < cutoffs[2])],
        series[series["size"] > cutoffs[2]],
    ]
    fits = [np.polyfit(subseries["size"], subseries["time"], 1)
            for subseries in subseriess]

    series = grouped_data[tuple(data["fitted_data_test_case"])]
    series = pd.DataFrame.from_dict(series)
    zooms = [(260, 9e-6, "B", 1), (35000, 8e-5, "KiB", 1024), (None, None, "KiB", 1024)]
    time_factor = 1e-6
    for j, (max_size, max_time, size_unit, size_factor) in enumerate(zooms):
        fig, ax = plt.subplots(figsize=figsize)
        ax.plot(
            series["size"] / size_factor,
            series["time"] / time_factor,
            "o",
            label=series["label"][0],
            color=series["color"][0],
            **plot_args)
        for i, fit in enumerate(data["fits"]):
            size = np.linspace(data["cutoffs"][i], data["cutoffs"][i + 1], 200)
            ax.plot(
                size / size_factor,
                np.poly1d(fit)(size) / time_factor,
                label="fit {0}".format(i + 1),
                color=[
                    "#f29312",
                    "#4caf50",
                    "#2196f3",
                ][i],
                **plot_args)
        ax.set_xlabel("array size /" + size_unit)
        ax.set_ylabel("time taken /us")
        if max_size is not None:
            ax.set_xlim(0, max_size / size_factor)
        if max_time is not None:
            ax.set_ylim(0, max_time / time_factor)
        ax.grid("on")
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        fig.savefig(fig_fns["fig_fit_{0}_fn".format(j)],
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
