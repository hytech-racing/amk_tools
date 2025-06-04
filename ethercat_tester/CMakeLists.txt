cmake_minimum_required(VERSION 3.28)

find_package(soem REQUIRED)

add_executable(read_param 
    src/main.cpp 
    src/programmer.cpp)

target_include_directories(read_param PRIVATE include)
target_link_libraries(read_param PUBLIC soem)

install(TARGETS read_param DESTINATION bin)