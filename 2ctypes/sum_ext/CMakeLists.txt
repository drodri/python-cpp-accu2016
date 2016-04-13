project(sum_ext C)
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/../../)

add_library(sum_ext SHARED sum.c)
