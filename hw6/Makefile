.POSIX:

CC=cc
CFLAGS=-Wall -O3 -fopenmp
LIBS=-lm

all: index.html

clean:
	rm -fr -- ../dist/bin/pcopy ../dist/tmp/hw6/pcopy.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o analysis.json bench.json figs.json index.html

../dist/bin/pcopy: ../dist/tmp/hw6/pcopy.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw6/pcopy.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o $(LIBS)

../dist/tmp/hw6/pcopy.o: ../utils/utils.h pcopy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o '$@' pcopy.c

../dist/tmp/utils/time.o: ../utils/time.c ../utils/time.h
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o '$@' ../utils/time.c

../dist/tmp/utils/utils.o: ../utils/time.h ../utils/utils.c ../utils/utils.h
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o '$@' ../utils/utils.c

Makefile: make.py
	makegen make.py

analysis.json: bench.json main.py
	python main.py analyze '$@' bench.json

bench.json: ../dist/bin/pcopy
	python main.py bench '$@' ../dist/bin/pcopy

figs.json: analysis.json main.py
	python main.py plot '$@' analysis.json

index.html: analysis.json figs.json main.py template.html
	python main.py report '$@' analysis.json figs.json template.html

.PHONY: all clean

.SECONDARY: ../dist/bin/pcopy ../dist/tmp/hw6/pcopy.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o analysis.json bench.json figs.json index.html
