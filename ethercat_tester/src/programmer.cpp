#include "programmer.h"

// #include <ethercatmain.h>

// extern "C"
// {
// #include "ethercat.h"
// }


std::optional<EtherCATConStatus> attempt_connection(std::string adapter_name)
{
    EtherCATConStatus status = {};

    if (ec_init(adapter_name.c_str()) <= 0) {
        printf("No EtherCAT adapter found.\n");
        return std::nullopt;
    }

    printf("Initializing EtherCAT master...\n");

    if (ec_slavecount > 0) {
        for (int i = 1; i <= ec_slavecount; i++) {
            printf("Configuring PDOs for Slave %d: %s\n", i, ec_slave[i].name);
            ec_slave[i].PO2SOconfig = [](uint16 slave) -> int {
                printf("Applying custom PDO mapping for Slave %d\n", slave);
                return 1; // Tell SOEM that mapping is valid
            };
        }
    }

    char IOmap[128];
    if (ec_config_init(FALSE) <= 0) {
        printf("No EtherCAT slaves found.\n");
        ec_close();
        return std::nullopt;
    }

    printf("%d slaves found and configured.\n", ec_slavecount);
    status.slavecount = ec_slavecount;

    // Map process data
    if (ec_config_map(&IOmap) <= 0) {
        printf("PDO mapping failed.\n");
        ec_close();
        return std::nullopt;
    }

    // Enable Distributed Clocks (DC) if required
    ec_configdc();
    ec_dcsync0(0, TRUE, 1000, 0); // SYNC0 on slave 1

    // ec_dcsync0(2, TRUE, 1000, 0); // SYNC0 on slave 1
    ec_readstate();
    printf("DC sync state: %d\n", ec_slave[1].state);
    
    // Transition to EC_STATE_INIT
    ec_slave[0].state = EC_STATE_INIT;
    ec_writestate(0);
    ec_statecheck(0, EC_STATE_INIT, EC_TIMEOUTSTATE);
    ec_readstate();

    // Print slave states after EC_STATE_INIT
    for (int i = 1; i <= ec_slavecount; i++) {
        printf("Slave %d: %s, State=0x%2.2X\n",
               i, ec_slave[i].name, ec_slave[i].state);

        // Check for AL Status errors
        if (ec_slave[i].ALstatuscode) {
            printf("AL Status Code: 0x%4.4X - %s\n",
                   ec_slave[i].ALstatuscode,
                   ec_ALstatuscode2string(ec_slave[i].ALstatuscode));
        }
    }
    // Transition to EC_STATE_PRE_OP
    ec_slave[0].state = EC_STATE_PRE_OP;
    ec_writestate(0);
    ec_statecheck(0, EC_STATE_PRE_OP, EC_TIMEOUTSTATE);
    ec_readstate();

    // Print slave states after EC_STATE_PRE_OP
    for (int i = 1; i <= ec_slavecount; i++) {
        printf("Slave %d: %s, State post pre-op=0x%2.2X\n",
               i, ec_slave[i].name, ec_slave[i].state);

        // Check for AL Status errors
        if (ec_slave[i].ALstatuscode) {
            printf("AL Status Code: 0x%4.4X - %s\n",
                   ec_slave[i].ALstatuscode,
                   ec_ALstatuscode2string(ec_slave[i].ALstatuscode));
        }
    }

    ec_slave[0].state = EC_STATE_SAFE_OP;
    ec_writestate(0);
    ec_statecheck(0, EC_STATE_SAFE_OP, EC_TIMEOUTSTATE);
    ec_readstate();

    // Print slave states after EC_STATE_SAFE_OP
    for (int i = 1; i <= ec_slavecount; i++) {
        printf("Slave %d: %s, State post EC_STATE_SAFE_OP=0x%2.2X\n",
               i, ec_slave[i].name, ec_slave[i].state);

        // Check for AL Status errors
        if (ec_slave[i].ALstatuscode) {
            printf("AL Status Code: 0x%4.4X - %s\n",
                   ec_slave[i].ALstatuscode,
                   ec_ALstatuscode2string(ec_slave[i].ALstatuscode));
        }
    }

    ec_slave[0].state = EC_STATE_OPERATIONAL;
    ec_writestate(0);
    ec_statecheck(0, EC_STATE_OPERATIONAL, EC_TIMEOUTSTATE);
    ec_readstate();

    // Print slave states after EC_STATE_OPERATIONAL
    for (int i = 1; i <= ec_slavecount; i++) {
        printf("Slave %d: %s, State post EC_STATE_OPERATIONAL=0x%2.2X\n",
               i, ec_slave[i].name, ec_slave[i].state);

        // Check for AL Status errors
        if (ec_slave[i].ALstatuscode) {
            printf("AL Status Code: 0x%4.4X - %s\n",
                   ec_slave[i].ALstatuscode,
                   ec_ALstatuscode2string(ec_slave[i].ALstatuscode));
        }
    }

    // Transition to EC_STATE_SAFE_OP
    // ec_slave[0].state = EC_STATE_SAFE_OP;
    // ec_writestate(0);
    // ec_statecheck(0, EC_STATE_SAFE_OP, EC_TIMEOUTSTATE);
    // ec_readstate();

    // // Print slave states after EC_STATE_SAFE_OP
    // for (int i = 1; i <= ec_slavecount; i++) {
    //     printf("Slave %d: %s, State post EC_STATE_SAFE_OP req=0x%2.2X\n",
    //            i, ec_slave[i].name, ec_slave[i].state);

    //     // Check for AL Status errors
    //     if (ec_slave[i].ALstatuscode) {
    //         printf("AL Status Code: 0x%4.4X - %s\n",
    //                ec_slave[i].ALstatuscode,
    //                ec_ALstatuscode2string(ec_slave[i].ALstatuscode));
    //     }
    // }

    // // Some slaves require SDO configuration before OP
    // for (int i = 1; i <= ec_slavecount; i++) {
    //     uint16_t index = 0x6060; // Example: Mode of Operation
    //     uint8_t subindex = 0x00;
    //     uint8_t mode = 3; // Check slave documentation for correct mode

    //     int wkc = ec_SDOwrite(i, index, subindex, FALSE, sizeof(mode), &mode, EC_TIMEOUTRXM);
    //     if (wkc <= 0) {
    //         printf("Warning: Failed to write SDO (0x6060) for Slave %d\n", i);
    //     }
    // }

    // Transition to OPERATIONAL state
    // ec_slave[0].state = EC_STATE_OPERATIONAL;
    // ec_writestate(0);
    // ec_statecheck(0, EC_STATE_OPERATIONAL, EC_TIMEOUTSTATE);
    // ec_readstate();?

    // // Print final state of slaves
    for (int i = 1; i <= ec_slavecount; i++) {
        printf("Slave %d: %s, State post=0x%2.2X\n",
               i, ec_slave[i].name, ec_slave[i].state);

        EtherCATSlave slave;
        slave.name = ec_slave[i].name;
        slave.state = static_cast<ec_state>(ec_slave[i].state);
        slave.address = ec_slave[i].configadr;
        status.slaves.push_back(slave);

        if (ec_slave[i].ALstatuscode) {
            printf("AL Status Code: 0x%4.4X - %s\n",
                   ec_slave[i].ALstatuscode,
                   ec_ALstatuscode2string(ec_slave[i].ALstatuscode));
        }
    }

    // Final check if at least one slave is in OP mode
    // bool allOperational = true;
    // for (const auto &slave : status.slaves) {
    //     if (slave.state != EC_STATE_OPERATIONAL) {
    //         allOperational = false;
    //         break;
    //     }
    // }

    // if (!allOperational) {
    //     printf("Not all slaves reached OPERATIONAL mode.\n");
    //     ec_close();
    //     return std::nullopt;
    // }

    // printf("All slaves successfully reached OPERATIONAL mode.\n");
    return status;
}

std::optional<std::vector<uint8_t>> read_sercos_param(uint16_t slave_index, uint16_t param_id, uint8_t subindex, size_t expected_size)
{
    // Example: Reading a SERCOS Parameter (SDO)
    // std::array<uint8_t, param_size> data;
    std::vector<uint8_t> data;
    int actual_size = expected_size;
    data.resize(expected_size);
    // uint16_t index = 0x6060; // Example index for mode of operation
    // uint8_t subindex = 0x00;
    uint32_t dat = 0;
    int data_size = sizeof(data);
    int wkc = ec_SDOread(slave_index, 0x6060, 0, FALSE, &data_size, &dat, EC_TIMEOUTRXM);
    if (wkc > 0)
    {
        std::cout << "size: " << data_size << std::endl;
        printf("Read SERCOS Parameter 0x%X: %u\n", param_id, data.data());
        return data;
    }
    else
    {
        std::cout << wkc<< std::endl;
        printf("SDO read failed\n");
        return std::nullopt;
    }

    ec_readstate();

    // Print slave states after EC_STATE_PRE_OP
    for (int i = 1; i <= ec_slavecount; i++) {
        // printf("Slave %d: %s, State post pre-op=0x%2.2X\n",
        //        i, ec_slave[i].name, ec_slave[i].state);

        // Check for AL Status errors
        if (ec_slave[i].ALstatuscode) {
            printf("AL Status Code: 0x%4.4X - %s\n",
                   ec_slave[i].ALstatuscode,
                   ec_ALstatuscode2string(ec_slave[i].ALstatuscode));
        }
    }
    return std::nullopt;
}