project(sumadl C)
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/../../)

add_library(sumadl SHARED suma.c)
