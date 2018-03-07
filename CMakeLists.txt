cmake_minimum_required(VERSION 3.5)
project(conan_ringbuffer)

include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

add_library(ringbuffer STATIC
    ./ringbuffer.c
)

target_include_directories(ringbuffer PRIVATE .)
