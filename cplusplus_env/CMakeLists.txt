cmake_minimum_required(VERSION 3.15)
project(cambio_cpp)
find_package(Python REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)
pybind11_add_module(cambio_cpp
    player.cpp
    cambio.cpp
    bindings.cpp
)
target_include_directories(cambio_cpp PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
