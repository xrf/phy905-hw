.POSIX:

CC=cc
CFLAGS=-O2 -mtune=native
STREAM_ARRAY_SIZE=16777216

all: ../dist/tmp/hw2/plot.ok index.html

clean:
	rm -fr -- ../dist/bin/hw2_copy_0000250 ../dist/bin/hw2_copy_0001000 ../dist/bin/hw2_copy_0005000 ../dist/bin/hw2_copy_0010000 ../dist/bin/hw2_copy_0050000 ../dist/bin/hw2_copy_0100000 ../dist/bin/hw2_copy_0500000 ../dist/bin/hw2_copy_1000000 ../dist/bin/hw2_copy_5000000 ../dist/bin/stream ../dist/tmp/ext/stream_BUXaw-oFf_eHA7HFeSUb.o ../dist/tmp/hw2/copy_0000250.o ../dist/tmp/hw2/copy_0001000.o ../dist/tmp/hw2/copy_0005000.o ../dist/tmp/hw2/copy_0010000.o ../dist/tmp/hw2/copy_0050000.o ../dist/tmp/hw2/copy_0100000.o ../dist/tmp/hw2/copy_0500000.o ../dist/tmp/hw2/copy_1000000.o ../dist/tmp/hw2/copy_5000000.o ../dist/tmp/hw2/plot.ok ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o data.json index.html report.txt

../dist/bin/hw2_copy_0000250: ../dist/tmp/hw2/copy_0000250.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_0000250.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/hw2_copy_0001000: ../dist/tmp/hw2/copy_0001000.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_0001000.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/hw2_copy_0005000: ../dist/tmp/hw2/copy_0005000.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_0005000.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/hw2_copy_0010000: ../dist/tmp/hw2/copy_0010000.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_0010000.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/hw2_copy_0050000: ../dist/tmp/hw2/copy_0050000.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_0050000.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/hw2_copy_0100000: ../dist/tmp/hw2/copy_0100000.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_0100000.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/hw2_copy_0500000: ../dist/tmp/hw2/copy_0500000.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_0500000.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/hw2_copy_1000000: ../dist/tmp/hw2/copy_1000000.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_1000000.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/hw2_copy_5000000: ../dist/tmp/hw2/copy_5000000.o ../dist/tmp/utils/time.o ../dist/tmp/utils/utils.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/hw2/copy_5000000.o ../dist/tmp/utils/utils.o ../dist/tmp/utils/time.o -lm

../dist/bin/stream: ../dist/tmp/ext/stream_BUXaw-oFf_eHA7HFeSUb.o
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CFLAGS) -o '$@' ../dist/tmp/ext/stream_BUXaw-oFf_eHA7HFeSUb.o

../dist/tmp/ext/stream_BUXaw-oFf_eHA7HFeSUb.o: ../ext/stream.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) '-DSTREAM_ARRAY_SIZE=$(STREAM_ARRAY_SIZE)' -c -o '$@' ../ext/stream.c

../dist/tmp/hw2/copy_0000250.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=250 -c -o '$@' copy.c

../dist/tmp/hw2/copy_0001000.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=1000 -c -o '$@' copy.c

../dist/tmp/hw2/copy_0005000.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=5000 -c -o '$@' copy.c

../dist/tmp/hw2/copy_0010000.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=10000 -c -o '$@' copy.c

../dist/tmp/hw2/copy_0050000.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=50000 -c -o '$@' copy.c

../dist/tmp/hw2/copy_0100000.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=100000 -c -o '$@' copy.c

../dist/tmp/hw2/copy_0500000.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=500000 -c -o '$@' copy.c

../dist/tmp/hw2/copy_1000000.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=1000000 -c -o '$@' copy.c

../dist/tmp/hw2/copy_5000000.o: ../utils/utils.h copy.c
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -DREPEATS=8 -DSIZE=5000000 -c -o '$@' copy.c

../dist/tmp/hw2/plot.ok: data.json
	@d=`dirname '$@'` && mkdir -p "$$d"
	./main.py plot '$@' data.json

../dist/tmp/utils/time.o: ../utils/time.c ../utils/time.h
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o '$@' ../utils/time.c

../dist/tmp/utils/utils.o: ../utils/time.h ../utils/utils.c ../utils/utils.h
	@d=`dirname '$@'` && mkdir -p "$$d"
	$(CC) $(CPPFLAGS) $(CFLAGS) -c -o '$@' ../utils/utils.c

data.json: ../dist/bin/hw2_copy_0000250 ../dist/bin/hw2_copy_0001000 ../dist/bin/hw2_copy_0005000 ../dist/bin/hw2_copy_0010000 ../dist/bin/hw2_copy_0050000 ../dist/bin/hw2_copy_0100000 ../dist/bin/hw2_copy_0500000 ../dist/bin/hw2_copy_1000000 ../dist/bin/hw2_copy_5000000
	./main.py bench '$@' ../dist/bin/hw2_copy_0000250 ../dist/bin/hw2_copy_0001000 ../dist/bin/hw2_copy_0005000 ../dist/bin/hw2_copy_0010000 ../dist/bin/hw2_copy_0050000 ../dist/bin/hw2_copy_0100000 ../dist/bin/hw2_copy_0500000 ../dist/bin/hw2_copy_1000000 ../dist/bin/hw2_copy_5000000

index.html: data.json report.txt template.html
	./main.py analyze '$@' data.json report.txt template.html

report.txt: ../dist/bin/stream
	../dist/bin/stream >'$@'.tmp && mv '$@'.tmp '$@'

.PHONY: all clean
