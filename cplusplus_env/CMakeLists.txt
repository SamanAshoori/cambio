cmake_minimum_required(VERSION 3.15)
project(player_cpp)

find_package(Python REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

pybind11_add_module(player_cpp
    player.cpp
    bindings.cpp
)

target_include_directories(player_cpp PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
