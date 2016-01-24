#!/usr/bin/env python
import re, string, sys
sys.path = ["../utils"] + list(sys.path)
from utils import *

def transpose(table):
    return list(zip(*table))

def substitute_template(filename, params):
    import string
    return string.Template(read_file(filename)).substitute(params)

def main_template(html):
    title = re.match("<h1>(.*)</h1>\n", html).group(1)
    return substitute_template("../utils/template.html", {
        "title": title,
        "body": html,
    })

def table_to_html(rows):
    s = []
    for row in rows:
        s.append("<tr>")
        for cell in row:
            s.extend(["<td>", str(cell), "</td>"])
        s.append("</tr>")
    return "".join(s)

def main():
    import json
    data = json.loads(read_file("data.json"))
    data["c1"] = "{:.3g}".format(data["c1"] * 1e9)
    data["c2"] = "{:.3g}".format(data["c2"] * 1e9)
    table = transpose(data["data"])
    table[1] = ["{:.0f}".format(x) for x in table[1]]
    table[3] = ["{:.3g}".format(x) for x in table[3]]
    table[4] = ["{:.3g}".format(x) for x in table[4]]
    data["data"] = table_to_html(transpose(table)).rstrip()
    write_file("index.html",
               main_template(substitute_template("template.html", data)))

main()
