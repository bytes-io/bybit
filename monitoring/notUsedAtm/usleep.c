// not used because GNU's sleep version  6.12 (at least and above) accepts floating point arguments. Could be used on a machine that does not have this fcn.

#include <unistd.h>
#include <stdlib.h>
int main(int argc, char **argv){
	usleep(atol(arfv[1]));
}
