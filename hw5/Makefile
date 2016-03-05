.POSIX:

all: ../ext/morth/morth1 index.html

bench: ../ext/morth/morth1
	../ext/morth/morth1 $(BENCHFLAGS)

clean:
	cd ../ext/morth && $(MAKE) clean
	rm -fr -- ../ext/morth/morth1 index.html

../ext/morth/morth1:
	@d=`dirname '$@'` && mkdir -p "$$d"
	cd ../ext/morth && $(MAKE)

Makefile: make.py
	@if command -v makegen >/dev/null 2>&1; then printf 'Updating makefile ...\n'; makegen make.py; else touch make.py; fi

index.html: main.py output.txt template.html vectorization.txt
	python main.py report '$@' template.html output.txt vectorization.txt

.PHONY: all bench clean

.SECONDARY: ../ext/morth/morth1 index.html
