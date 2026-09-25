CC ?= gcc
CFLAGS ?= -O2 -Wall
LDFLAGS ?= -lfec

# Si libfec ou libcorrect est installé dans /usr/local ou radioconda :
INCLUDES ?= -I/usr/local/include -I/usr/include
LIBDIRS  ?= -L/usr/local/lib -L/usr/lib

all: jmf_viterb

jmf_viterb: jmf_viterb.c
	@# Test de compilation avec la bibliothèque système ou locale
	@if [ -f "./libfec/libfec.a" ]; then \
		echo "Compilation statique avec ./libfec/libfec.a..."; \
		$(CC) $(CFLAGS) -o $@ jmf_viterb.c -I./libfec ./libfec/libfec.a; \
	elif [ -d "/home/lavarenne/radioconda/include" ]; then \
		echo "Compilation avec libfec de radioconda..."; \
		$(CC) $(CFLAGS) -o $@ -D"set_viterbi27_polynomial(x)=" jmf_viterb.c -I/home/lavarenne/radioconda/include -L/home/lavarenne/radioconda/lib -lfec -Wl,-rpath=/home/lavarenne/radioconda/lib; \
	else \
		echo "Compilation standard avec -lfec..."; \
		$(CC) $(CFLAGS) -o $@ jmf_viterb.c $(INCLUDES) $(LIBDIRS) $(LDFLAGS); \
	fi

clean:
	rm -f jmf_viterb entreeViterbi.bin sortieViterbi.bin

.PHONY: all clean
