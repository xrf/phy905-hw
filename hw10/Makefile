SCRATCH=/scratch/training/$$USER/phy905-hw10

all: ../dist/bin/ioda

../dist/bin/ioda: ../ext/ioda.c
	echo "SCRATCH=$(SCRATCH)" >../dist/tmp/ioda-vars.sh
	$(CC) $(CPPFLAGS) $(CFLAGS) \
	    -DMYSCRATCHDIR=\""$(SCRATCH)"\" \
	    -o $@ ../ext/ioda.c

clean:
	rm -f ../dist/bin/ioda ../dist/tmp/ioda-vars.sh
