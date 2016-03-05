from makegen import *

def make_all():
    return alias("all", [build(), report()]).merge(
        simple_command(
            "@if command -v makegen >/dev/null 2>&1; then "
            "printf 'Updating makefile ...\\n'; makegen {0}; else "
            "touch {0}; fi",
            "Makefile", ["make.py"], no_clean=True),
        bench(),
    )

def build():
    return simple_command(
        "cd ../ext/morth && $(MAKE)",
        "../ext/morth/morth1",
        [],
    ).merge(Ruleset(clean_cmds=["cd ../ext/morth && $(MAKE) clean"]))

def bench():
    return simple_command(
        "{0} $(BENCHFLAGS)",
        "bench",
        [build()],
        phony=True,
    )

def report():
    return simple_command(
        "python {0} report {out} {all1}",
        "index.html",
        ["main.py", "template.html", "output.txt", "vectorization.txt"],
    )

make_all().save()
