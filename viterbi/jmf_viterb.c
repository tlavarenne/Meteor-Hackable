// adaptation du script utilisé par JM Friedt
// gcc -o jmf_libfec jmf_libfec.c -I./libfec ./libfec/libfec.a 
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h> // read
#include <fec.h>
#define MAXBYTES (819200/16)  // Indiquer taille en octet du fichier à traiter /16
#define VITPOLYA 0x4F
#define VITPOLYB 0x6D
int viterbiPolynomial[2] = {VITPOLYA, VITPOLYB};
int main(int argc,char *argv[]){
  int i,framebits,fd;
  unsigned char data[MAXBYTES],*symbols; // [8*2*(MAXBYTES+6)]; // *8 for bytes->bits & *2 Viterbi
  void *vp;
  symbols=(unsigned char*)malloc(8*2*(MAXBYTES+6));
  fd=open("./entreeViterbi.bin",O_RDONLY); read(fd,symbols,MAXBYTES*16); close(fd);
	//for (i=0;i<MAXBYTES*16;i+=1) symbols[i]=-symbols[i];    //libfec require symbols inversion (uint8_t and int8_t conversion)
	//for (i=0;i<MAXBYTES*16;i+=2) symbols[i+1]=-symbols[i+1];    //Q inversion (most popular convention used by meteor)
  framebits = MAXBYTES*8;
  set_viterbi27_polynomial(viterbiPolynomial);
  vp=create_viterbi27(framebits);
  init_viterbi27(vp,0);
  update_viterbi27_blk(vp,symbols,framebits);
  chainback_viterbi27(vp,data,framebits,0);
  fd=open("./sortieViterbi.bin",O_WRONLY|O_CREAT,S_IRWXU|S_IRWXG|S_IRWXO); 
  write(fd,data,framebits/8);
  close(fd);
  exit(0);}
