CC=mpicc
CFLAGS=-Wall -Wextra -O3 -g
LIBS=-lm
WSIZE=4

all: index.html

bench: bench_1_000000.txt bench_1_000004.txt bench_1_000008.txt bench_1_000016.txt bench_1_000032.txt bench_1_000064.txt bench_1_000128.txt bench_1_000256.txt bench_1_000512.txt bench_1_001024.txt bench_1_002048.txt bench_1_004096.txt bench_1_008192.txt bench_1_016384.txt bench_1_032768.txt bench_1_065536.txt bench_1_131072.txt bench_1_262144.txt bench_2_000000.txt bench_2_000004.txt bench_2_000008.txt bench_2_000016.txt bench_2_000032.txt bench_2_000064.txt bench_2_000128.txt bench_2_000256.txt bench_2_000512.txt bench_2_001024.txt bench_2_002048.txt bench_2_004096.txt bench_2_008192.txt bench_2_016384.txt bench_2_032768.txt bench_2_065536.txt bench_2_131072.txt bench_2_262144.txt bench_3_000000.txt bench_3_000004.txt bench_3_000008.txt bench_3_000016.txt bench_3_000032.txt bench_3_000064.txt bench_3_000128.txt bench_3_000256.txt bench_3_000512.txt bench_3_001024.txt bench_3_002048.txt bench_3_004096.txt bench_3_008192.txt bench_3_016384.txt bench_3_032768.txt bench_3_065536.txt bench_3_131072.txt bench_3_262144.txt

clean:
	rm -fr -- ../dist/bin/mpicomm ../dist/tmp/hw8/mpicomm.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o analysis.json bench_1_000000.txt bench_1_000004.txt bench_1_000008.txt bench_1_000016.txt bench_1_000032.txt bench_1_000064.txt bench_1_000128.txt bench_1_000256.txt bench_1_000512.txt bench_1_001024.txt bench_1_002048.txt bench_1_004096.txt bench_1_008192.txt bench_1_016384.txt bench_1_032768.txt bench_1_065536.txt bench_1_131072.txt bench_1_262144.txt bench_2_000000.txt bench_2_000004.txt bench_2_000008.txt bench_2_000016.txt bench_2_000032.txt bench_2_000064.txt bench_2_000128.txt bench_2_000256.txt bench_2_000512.txt bench_2_001024.txt bench_2_002048.txt bench_2_004096.txt bench_2_008192.txt bench_2_016384.txt bench_2_032768.txt bench_2_065536.txt bench_2_131072.txt bench_2_262144.txt bench_3_000000.txt bench_3_000004.txt bench_3_000008.txt bench_3_000016.txt bench_3_000032.txt bench_3_000064.txt bench_3_000128.txt bench_3_000256.txt bench_3_000512.txt bench_3_001024.txt bench_3_002048.txt bench_3_004096.txt bench_3_008192.txt bench_3_016384.txt bench_3_032768.txt bench_3_065536.txt bench_3_131072.txt bench_3_262144.txt figs.json index.html

../dist/bin/mpicomm: ../dist/tmp/hw8/mpicomm.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@mkdir -p "`dirname $@`"
	$(CC) $(CFLAGS) -o $@ ../dist/tmp/hw8/mpicomm.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o $(LIBS)

../dist/tmp/hw8/mpicomm.o: ../utils/utils.h mpicomm.c
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ mpicomm.c

../dist/tmp/utils/time.o: ../utils/time.c ../utils/time.h
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ ../utils/time.c

../dist/tmp/utils/utils.o: ../utils/time.h ../utils/utils.c ../utils/utils.h
	@mkdir -p "`dirname $@`"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o $@ ../utils/utils.c

analysis.json: bench_1_000000.txt bench_1_000004.txt bench_1_000008.txt bench_1_000016.txt bench_1_000032.txt bench_1_000064.txt bench_1_000128.txt bench_1_000256.txt bench_1_000512.txt bench_1_001024.txt bench_1_002048.txt bench_1_004096.txt bench_1_008192.txt bench_1_016384.txt bench_1_032768.txt bench_1_065536.txt bench_1_131072.txt bench_1_262144.txt bench_2_000000.txt bench_2_000004.txt bench_2_000008.txt bench_2_000016.txt bench_2_000032.txt bench_2_000064.txt bench_2_000128.txt bench_2_000256.txt bench_2_000512.txt bench_2_001024.txt bench_2_002048.txt bench_2_004096.txt bench_2_008192.txt bench_2_016384.txt bench_2_032768.txt bench_2_065536.txt bench_2_131072.txt bench_2_262144.txt bench_3_000000.txt bench_3_000004.txt bench_3_000008.txt bench_3_000016.txt bench_3_000032.txt bench_3_000064.txt bench_3_000128.txt bench_3_000256.txt bench_3_000512.txt bench_3_001024.txt bench_3_002048.txt bench_3_004096.txt bench_3_008192.txt bench_3_016384.txt bench_3_032768.txt bench_3_065536.txt bench_3_131072.txt bench_3_262144.txt main.py
	python main.py analyze '$@' bench_1_000000.txt bench_1_000004.txt bench_1_000008.txt bench_1_000016.txt bench_1_000032.txt bench_1_000064.txt bench_1_000128.txt bench_1_000256.txt bench_1_000512.txt bench_1_001024.txt bench_1_002048.txt bench_1_004096.txt bench_1_008192.txt bench_1_016384.txt bench_1_032768.txt bench_1_065536.txt bench_1_131072.txt bench_1_262144.txt bench_2_000000.txt bench_2_000004.txt bench_2_000008.txt bench_2_000016.txt bench_2_000032.txt bench_2_000064.txt bench_2_000128.txt bench_2_000256.txt bench_2_000512.txt bench_2_001024.txt bench_2_002048.txt bench_2_004096.txt bench_2_008192.txt bench_2_016384.txt bench_2_032768.txt bench_2_065536.txt bench_2_131072.txt bench_2_262144.txt bench_3_000000.txt bench_3_000004.txt bench_3_000008.txt bench_3_000016.txt bench_3_000032.txt bench_3_000064.txt bench_3_000128.txt bench_3_000256.txt bench_3_000512.txt bench_3_001024.txt bench_3_002048.txt bench_3_004096.txt bench_3_008192.txt bench_3_016384.txt bench_3_032768.txt bench_3_065536.txt bench_3_131072.txt bench_3_262144.txt

bench_1_000000.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 0 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_000004.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 4 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_000008.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 8 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_000016.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 16 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_000032.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 32 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_000064.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 64 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_000128.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 128 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_000256.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 256 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_000512.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 512 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_001024.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 1024 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_002048.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 2048 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_004096.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 4096 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_008192.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 8192 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_016384.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 16384 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_032768.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 32768 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_065536.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 65536 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_131072.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 131072 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_1_262144.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 1 262144 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000000.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 0 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000004.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 4 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000008.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 8 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000016.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 16 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000032.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 32 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000064.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 64 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000128.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 128 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000256.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 256 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_000512.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 512 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_001024.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 1024 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_002048.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 2048 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_004096.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 4096 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_008192.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 8192 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_016384.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 16384 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_032768.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 32768 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_065536.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 65536 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_131072.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 131072 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_2_262144.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 0 `expr $(WSIZE) - 1` 262144 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000000.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 0 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000004.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 4 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000008.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 8 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000016.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 16 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000032.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 32 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000064.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 64 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000128.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 128 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000256.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 256 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_000512.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 512 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_001024.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 1024 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_002048.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 2048 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_004096.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 4096 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_008192.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 8192 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_016384.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 16384 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_032768.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 32768 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_065536.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 65536 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_131072.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 131072 | tee '$@'.tmp && mv '$@'.tmp '$@'

bench_3_262144.txt: ../dist/bin/mpicomm
	mpiexec -np $(WSIZE) ../dist/bin/mpicomm 2 3 262144 | tee '$@'.tmp && mv '$@'.tmp '$@'

figs.json: analysis.json main.py
	python main.py plot '$@' analysis.json

index.html: analysis.json figs.json main.py template.html
	python main.py report '$@' analysis.json figs.json template.html

.PHONY: all bench clean
