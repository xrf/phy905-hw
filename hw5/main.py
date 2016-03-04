#!/usr/bin/env python
import logging, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

FIGSIZE = (5, 3.5)

@register_command(commands)
def bench(out_fn, exe):
    import re
    bsize, size, optlevel = re.match(r".*?_(\d+)_(\d+)_(\d+)$", exe).groups()
    logging.info("Benchmarking with "
                 "BSIZE = {0}, SIZE = {1}, OPTLEVEL = {2} ..."
                 .format(bsize, size, optlevel))
    out = run_and_get_keyvalues([exe])
    save_json_file(out_fn, {
        "bsize": int(bsize),
        "size": int(size),
        "optlevel": int(optlevel),
        "time_min": float(out["min"]),
        "time_mean": float(out["mean"]),
        "time_stdev": float(out["stdev"]),
        "num_subrepeats": int(out["num_subrepeats"]),
    }, json_args=JSON_ARGS)

@register_command(commands)
def merge(out_fn, *fns):
    data = records_to_dataframe(load_json_file(fn) for fn in fns)
    save_json_file(out_fn, data, json_args=JSON_ARGS)

def analyze_group(series, group):
    group.sort(key=lambda x: x["size"])
    group = records_to_dataframe(group)
    size = np.array(group["size"])
    time = np.array(group["time_mean"])
    time_err = np.array(group["time_stdev"])
    performance = 2 * size ** 3 / time
    performance_err = performance * time_err / time
    series.update({
        "size": size.tolist(),
        "time": time.tolist(),
        "time_err": time_err.tolist(),
        "performance": performance.tolist(),
        "performance_err": performance_err.tolist(),
    })

@register_command(commands)
def analyze(out_fn, fn):
    records = dataframe_to_records(load_json_file(fn))
    groups = group_records_by(records, ["optlevel", "bsize"])
    data = []
    for (optlevel, bsize), group in sorted(groups.items()):
        series = {
            "color": {
                0: "#e91e63",
                1: "#f29312",
                2: "#4caf50",
                3: "#2196f3",
            }[optlevel],
            "linestyle": "--" if (bsize or 1) > 1 else "-",
            "label": "-O{0}{1}".format(
                optlevel,
                " blocked" if (bsize or 1) > 1 else "",
            ),
        }
        analyze_group(series, group)
        data.append(series)
    save_json_file(out_fn, data, json_args=JSON_ARGS)

@register_command(commands)
def analyze_series(out_fn, *fns):
    import os
    data = []
    for fn in fns:
        label = os.path.splitext(os.path.basename(fn))[0]
        records = dataframe_to_records(load_json_file(fn))
        group = group_records_by(records, ["optlevel"])[(3,)]
        group = [x for x in group if x["bsize"] > 1 or x["bsize"] is None]
        series = {
            "color": {
                "gcc-data": "#e91e63",
                "clang-data": "#f29312",
                "eigen-data": "#4caf50",
                "openblas-data": "#2196f3",
                "openblas-4threads-data": "#1a237e",
            }.get(label, None),
            "label": label,
        }
        analyze_group(series, group)
        data.append(series)
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
        "fig_compare_fn": "fig-compare.svg",
    }

    fig, ax = plt.subplots(figsize=FIGSIZE)
    for series in data:
        ax.errorbar(
            series["size"],
            series["time"],
            yerr=series["time_err"],
            label=series["label"],
            color=series.get("color", None),
            linestyle=series.get("linestyle", "-"),
            **plot_args
        )
    ax.set_xlabel("matrix size (n)")
    ax.set_ylabel("time taken /s")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.grid("on")
    legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    fig.savefig(fig_fns["fig_time_fn"],
                bbox_extra_artists=(legend,),
                bbox_inches="tight",
                transparent=True)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    for series in data:
        ax.errorbar(
            series["size"],
            np.array(series["performance"]) / 1e9,
            yerr=np.array(series["performance_err"]) / 1e9,
            label=series["label"],
            color=series.get("color", None),
            linestyle=series.get("linestyle", "-"),
            **plot_args
        )
    ax.set_xlabel("matrix size (n)")
    ax.set_ylabel("effective performance /GFLOPS")
    ax.set_xscale("log")
    ax.grid("on")
    legend = ax.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    fig.tight_layout()
    fig.savefig(fig_fns["fig_compare_fn"],
                bbox_extra_artists=(legend,),
                bbox_inches="tight",
                transparent=True)

    save_json_file(out_fn, fig_fns, json_args=JSON_ARGS)

@register_command(commands)
def report(out_fn, data_fn, figs_fn, template_fn):
    import cgi
    data = load_json_file(data_fn)
    table = ([["{0}".format(x) for x in data[0]["size"]]] +
             [["{0:.3g}".format(x) for x in series["time"]]
              for series in data])
    params = load_json_file(figs_fn)
    params["code"] = cgi.escape(load_file("multiply_blocked.c"))
    params["data"] = table_to_html(transpose(table)).rstrip()
    html = main_template(substitute_template(template_fn, params))
    save_file(out_fn, html)

@register_command(commands)
def combine(out_fn, fn, num_repeats):
    records = dataframe_to_records(load_json_file(fn))
    groups = sorted(group_records_by(records, ["bsize"]).items())
    _, group0 = groups[0]
    group0.sort(key=lambda x: (x["optlevel"], x["size"]))
    data = records_to_dataframe(group0)
    num_repeats = np.full_like(data["time_mean"], num_repeats)
    data["num_repeats"] = data.get("num_repeats", num_repeats)
    data["bsize"] = [None] * len(data["num_repeats"])
    del data["num_subrepeats"]
    for (bsize,), group in groups[1:]:
        group.sort(key=lambda x: (x["optlevel"], x["size"]))
        group = records_to_dataframe(group)
        assert data["size"] == group["size"]
        assert data["optlevel"] == group["optlevel"]
        data["time_min"] = np.minimum(np.array(data["time_min"]),
                                      np.array(group["time_min"]))
        (
            data["num_repeats"],
            data["time_mean"],
            data["time_stdev"],
        ) = merge_stdevs(
            np.array(data["num_repeats"]),
            np.array(data["time_mean"]),
            np.array(data["time_stdev"]),
            group.get("num_repeats", num_repeats),
            np.array(group["time_mean"]),
            np.array(group["time_stdev"]),
        )
    for k in ["num_repeats", "time_min", "time_mean", "time_stdev"]:
        data[k] = data[k].tolist()
    save_json_file(out_fn, data, json_args=JSON_ARGS)

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
