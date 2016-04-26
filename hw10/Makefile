SCRATCH=/scratch/training/$$USER/phy905-hw10

all: index.html

build: ../dist/bin/ioda

index.html: main.py index.md data.txt
	./main.py report $@ index.md data.txt

../dist/bin/ioda: ../ext/ioda.c
	echo "SCRATCH=$(SCRATCH)" >../dist/tmp/ioda-vars.sh
	$(CC) $(CPPFLAGS) $(CFLAGS) \
	    -DMYSCRATCHDIR=\""$(SCRATCH)/"\" \
	    -o $@ ../ext/ioda.c

clean:
	rm -f index.html ../dist/bin/ioda ../dist/tmp/ioda-vars.sh
