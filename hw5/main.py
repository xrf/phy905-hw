#!/usr/bin/env python
import cgi, logging, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path = ["../utils"] + list(sys.path)
from utils import *
commands = {}

@register_command(commands)
def report(out_fn, template_fn, output_fn, vectorization_fn):
    params = {
        "output": cgi.escape(load_file(output_fn)),
        "vectorization": cgi.escape(load_file(vectorization_fn)),
    }
    html = main_template(substitute_template(template_fn, params))
    save_file(out_fn, html)

def main():
    init_logging(default_level=logging.INFO)
    run_command(commands)

if __name__ == "__main__":
    main()
