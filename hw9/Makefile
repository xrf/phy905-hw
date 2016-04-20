CFLAGS=-O3 -g
CPPFLAGS=-DNDEBUG -I../utils/blas
LIBS=-lm

all: index.html

build: ../dist/bin/mpibandwidth ../dist/bin/mpigemv

clean:
	rm -fr -- ../dist/bin/mpibandwidth ../dist/bin/mpigemv ../dist/tmp/hw9/mpibandwidth.o ../dist/tmp/hw9/mpigemv.o ../dist/tmp/utils/blas/dgemv.o ../dist/tmp/utils/mpi.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o analysis.json figs.json index.html

../dist/bin/mpibandwidth: ../dist/tmp/hw9/mpibandwidth.o ../dist/tmp/utils/mpi.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@mkdir -p "`dirname $@`"
	$(CC) $(CFLAGS) -o $@ ../dist/tmp/hw9/mpibandwidth.o ../dist/tmp/utils/mpi.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o $(LIBS)

../dist/bin/mpigemv: ../dist/tmp/hw9/mpigemv.o ../dist/tmp/utils/blas/dgemv.o ../dist/tmp/utils/mpi.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@mkdir -p "`dirname $@`"
	$(CC) $(CFLAGS) -o $@ ../dist/tmp/hw9/mpigemv.o ../dist/tmp/utils/mpi.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/blas/dgemv.o $(LIBS)

../dist/tmp/hw9/mpibandwidth.o:  ../utils/compat/noreturn_begin.h ../utils/compat/noreturn_end.h ../utils/mpi.h ../utils/utils.h mpibandwidth.c
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ mpibandwidth.c

../dist/tmp/hw9/mpigemv.o:  ../utils/compat/noreturn_begin.h ../utils/compat/noreturn_end.h ../utils/mpi.h ../utils/utils.h mpigemv.c
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ mpigemv.c

../dist/tmp/utils/blas/dgemv.o: ../utils/blas/dgemv.c
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ ../utils/blas/dgemv.c

../dist/tmp/utils/mpi.o:  ../utils/compat/noreturn_begin.h ../utils/compat/noreturn_end.h ../utils/mpi.c ../utils/mpi.h ../utils/utils.h
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ ../utils/mpi.c

../dist/tmp/utils/time.o: ../utils/time.c ../utils/time.h
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ ../utils/time.c

../dist/tmp/utils/utils.o:  ../utils/compat/noreturn_begin.h ../utils/compat/noreturn_end.h ../utils/time.h ../utils/utils.c ../utils/utils.h
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ ../utils/utils.c

analysis.json: main.py
	python main.py analyze '$@'

figs.json: analysis.json main.py
	python main.py plot '$@' analysis.json

index.html: analysis.json figs.json index.md main.py
	python main.py report '$@' analysis.json figs.json index.md

.PHONY: all build clean
