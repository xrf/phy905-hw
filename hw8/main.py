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
    grouped_data = []
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
            "label": "test={1},case={0}".format(test, case),
        }
        series.update(records_to_dataframe(group))
        grouped_data.append(series)
    save_json_file(out_fn, {
        "data": data,
        "grouped_data": grouped_data,
    }, json_args=JSON_ARGS)

@register_command(commands)
def plot(out_fn, data_fn):
    plot_args = {
        "alpha": .8,
        "linewidth": 2,
        "markeredgecolor": "none",
    }
    data = load_json_file(data_fn)["grouped_data"]
    figsize = (5, 3.5)
    fig_fns = {
        "fig_time_fn": "fig-time.svg",
        "fig_time_zoomed_fn": "fig-time-zoomed.svg",
    }
    ZOOMED_SIZE_MAX = 32

    for zoomed in ["", "_zoomed"]:
        fig, ax = plt.subplots(figsize=figsize)
        for series in data:
            series = pd.DataFrame.from_dict(series)
            if zoomed:
                series = series[series["size"] <= ZOOMED_SIZE_MAX]
                series["time"] *= 1e6
            ax.errorbar(
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
        fig.tight_layout()
        legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        fig.tight_layout()
        fig.savefig(fig_fns["fig_time{0}_fn".format(zoomed)],
                    bbox_extra_artists=(legend,),
                    bbox_inches="tight",
                    transparent=True)

    save_json_file(out_fn, fig_fns, json_args=JSON_ARGS)

@register_command(commands)
def report(out_fn, data_fn, figs_fn, template_fn):
    import cgi
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
    html = main_template(substitute_template(template_fn, params))
    save_file(out_fn, html)

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
