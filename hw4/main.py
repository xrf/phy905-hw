#!/usr/bin/env python
import logging, sys
import matplotlib.pyplot as plt
import numpy as np
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

@register_command(commands)
def analyze(out_fn, fn):
    records = dataframe_to_records(load_json_file(fn))
    groups = group_records_by(records, ["optlevel", "bsize"])
    data = []
    for (optlevel, bsize), group in sorted(groups.items()):
        group.sort(key=lambda x: x["size"])
        group = records_to_dataframe(group)
        size = np.array(group["size"])
        time = np.array(group["time_mean"])
        time_err = np.array(group["time_stdev"])
        performance = 2 * size ** 3 / time
        performance_err = performance * time_err / time
        data.append({
            "size": size.tolist(),
            "time": time.tolist(),
            "time_err": time_err.tolist(),
            "performance": performance.tolist(),
            "performance_err": performance_err.tolist(),
            "color": {
                0: "#e91e63",
                1: "#f29312",
                2: "#4caf50",
                3: "#2196f3",
            }[optlevel],
            "linestyle": "--" if bsize > 1 else "-",
            "label": "-O{0}{1}".format(
                optlevel,
                " blocked" if bsize > 1 else "",
            ),
        })
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
            label=series["label"],
            color=series["color"],
            linestyle=series["linestyle"],
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
            label=series["label"],
            color=series["color"],
            linestyle=series["linestyle"],
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

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
