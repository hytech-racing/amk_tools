#ifndef __PROGRAMMER_H__
#define __PROGRAMMER_H__

#include "ethercat.h" // because of sins, this must be included first

#include <optional>
#include <array>
#include <vector>

#include <cstdint>
#include <string>

#include <iostream>

// USAGE:

// 1. must attempt connection
// 2. if connection successful, the connection is still be open and you can run the read or write operation, else it will be closed
// 3. 
struct EtherCATSlave
{
    ec_state state;
    uint16_t address;
    std::string name;
};
struct EtherCATConStatus
{
    size_t slavecount;
    std::vector<EtherCATSlave> slaves;
};

// 
std::optional<EtherCATConStatus> attempt_connection(std::string adapter_name);

template<size_t param_size>
bool write_sercos_param(uint16_t slave_index, uint16_t param_id, uint8_t subindex, std::array<uint8_t, param_size> param_data)
{
    return true;
}

std::optional<std::vector<uint8_t>> read_sercos_param(uint16_t slave_index, uint16_t param_id, uint8_t subindex, size_t expected_size);
#endif // __PROGRAMMER_H__