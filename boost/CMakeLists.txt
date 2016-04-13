cmake_minimum_required(VERSION 2.8)
project(BoostPython)

set (CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/../../)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

include_directories("C:/Python27/include")
link_directories("C:/Python27/libs")

add_library(boost_python SHARED main.cpp)
