#!/usr/bin/env python
import glob, json, logging, os, re, subprocess, sys, tempfile
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

@register_command(commands)
def report(out_fn, index_fn, data_fn):
    template_fn = out_fn + ".tmp"
    with open(data_fn) as f:
        rows = [line.split("\t") for line in f]
    table = [[
        str(int(row[0])),
        "{0:.3g}".format(float(row[1])),
        "{0:.3g}".format(float(row[2])),
        "{0:.3g}".format(float(row[3]) - float(row[2])),
        "{0:.3g}".format(float(row[4]) / 1e9),
    ] for row in rows]
    params = {
        "data": table_to_html(table).rstrip(),
    }
    with tempfile.NamedTemporaryFile(mode="wt") as f:
        subprocess.check_call(["pandoc", "-f", "commonmark",
                               "-t", "html", "-o", f.name, index_fn])
        html = main_template(substitute_template(f.name, params))
    save_file(out_fn, html)

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
