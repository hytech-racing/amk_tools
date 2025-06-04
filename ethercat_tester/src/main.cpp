#include "programmer.h"
#include <cstddef>
#include <ethercattype.h>

int main(int argc, char *argv[]) {
  if (argc > 1) {
    printf("SOEM (Simple Open EtherCAT Master)\nSimple test\n");
    if (ec_init(argv[1]) > 0) {
      if (ec_config_init(FALSE) > 0) {
        printf("%d slaves found and configured.\n", ec_slavecount);
        char IOmap[128];
        int  usedmem;
        usedmem = ec_config_map(&IOmap);
        if (usedmem <= sizeof(IOmap))
        {
            ec_send_processdata();
            wkc = ec_receive_processdata(EC_TIMEOUTRET);
        }
      }
    }
  }
}