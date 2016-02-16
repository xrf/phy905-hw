#!/usr/bin/env python
import logging, sys
import matplotlib.pyplot as plt
import numpy as np
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

FIGSIZE = (6, 4)

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
    })

@register_command(commands)
def merge(out_fn, *fns):
    records = tuple(load_json_file(fn) for fn in fns)
    groups = group_records_by(records, ["optlevel", "bsize"])
    data = []
    for (optlevel, bsize), group in groups.items():
        group.sort(key=lambda x: x["size"])
        group = records_to_dataframe(group)
        size = np.array(group["size"])
        time = np.array(group["time_mean"])
        data.append({
            "size": size.tolist(),
            "time": time.tolist(),
            "performance": (2 * size ** 3 / time).tolist(),
            "fmt": "x-",
            "label": "-O{0}{1}".format(
                optlevel,
                " blocked" if bsize > 1 else "",
            ),
        })
    save_json_file(out_fn, data)

@register_command(commands)
def plot(out_fn, data_fn):
    data = load_json_file(data_fn)

    fig_fns = {
        "fig_time_fn": "fig-time.svg",
        "fig_compare_fn": "fig-compare.svg",
    }

    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot = ax.loglog
    for series in data:
        plot(series["size"], series["time"],
             series["fmt"], label=series["label"])
    ax.set_xlabel("matrix size (n)")
    ax.set_ylabel("time taken /s")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(fig_fns["fig_time_fn"], transparent=True)

    fig, ax = plt.subplots(figsize=FIGSIZE)
    plot = ax.semilogx
    for series in data:
        plot(series["size"], np.array(series["performance"]) / 1e9,
             series["fmt"], label=series["label"])
    ax.set_xlabel("matrix size (n)")
    ax.set_ylabel("effective performance /GFLOPS")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(fig_fns["fig_compare_fn"], transparent=True)

    save_json_file(out_fn, fig_fns)

@register_command(commands)
def report(out_fn, data_fn, figs_fn, template_fn):
    import cgi
    data = load_json_file(data_fn)
    table = ([["{0}".format(x) for x in data[0]["size"]]] +
             [["{0:.3g}".format(x) for x in series["time"]]
              for series in data])
    params = load_json_file(figs_fn)
    params["data"] = table_to_html(transpose(table)).rstrip()
    html = main_template(substitute_template(template_fn, params))
    save_file(out_fn, html)

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
