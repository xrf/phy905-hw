build:
	./main.py -q --data data.json --fig-perf fig-perf.svg --fig-time fig-time.svg
	./table.py

mmc: mmc.c
	@mkdir -p `dirname $@`
	$(CC) -O2 -mtune=native -o $@ mmc.c
