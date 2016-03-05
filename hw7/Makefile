.POSIX:

CFLAGS=-Wall -O3
FOPENMP=-fopenmp
LIBS=-lm

all: index.html

clean:
	rm -fr -- ../dist/bin/pmultiply ../dist/bin/pmultiply_omp ../dist/tmp/hw7/pmultiply.o ../dist/tmp/hw7/pmultiply_ADK9YFxZhXVt_AeKjCgX.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o analysis.json bench.json figs.json index.html

../dist/bin/pmultiply: ../dist/tmp/hw7/pmultiply.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw7/pmultiply.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o $(LIBS)

../dist/bin/pmultiply_omp: ../dist/tmp/hw7/pmultiply_ADK9YFxZhXVt_AeKjCgX.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw7/pmultiply_ADK9YFxZhXVt_AeKjCgX.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o $(FOPENMP) $(LIBS)

../dist/tmp/hw7/pmultiply.o: ../utils/utils.h pmultiply.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o '$@' pmultiply.c

../dist/tmp/hw7/pmultiply_ADK9YFxZhXVt_AeKjCgX.o: ../utils/utils.h pmultiply.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) '$(FOPENMP)' -c -o '$@' pmultiply.c

../dist/tmp/utils/time.o: ../utils/time.c ../utils/time.h
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o '$@' ../utils/time.c

../dist/tmp/utils/utils.o: ../utils/time.h ../utils/utils.c ../utils/utils.h
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o '$@' ../utils/utils.c

Makefile: make.py
	@if command -v makegen >/dev/null 2>&1; then printf 'Updating makefile ...\n'; makegen make.py; else touch make.py; fi

analysis.json: bench.json main.py
	python main.py analyze '$@' bench.json

bench.json: ../dist/bin/pmultiply ../dist/bin/pmultiply_omp
	python main.py bench '$@' ../dist/bin/pmultiply ../dist/bin/pmultiply_omp

figs.json: analysis.json main.py
	python main.py plot '$@' analysis.json

index.html: analysis.json figs.json main.py template.html
	python main.py report '$@' analysis.json figs.json template.html

.PHONY: all clean

.SECONDARY: ../dist/bin/pmultiply ../dist/bin/pmultiply_omp ../dist/tmp/hw7/pmultiply.o ../dist/tmp/hw7/pmultiply_ADK9YFxZhXVt_AeKjCgX.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o analysis.json bench.json figs.json index.html
