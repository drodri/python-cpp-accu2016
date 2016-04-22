cmake_minimum_required(VERSION 2.8.12)
project(sum_ext C)

set (CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR}/../)
include_directories("C:/Python27/include")
link_directories("C:/Python27/libs")
add_library(_sum SHARED sum.c sum_wrap.c)
if(MSVC)
  set_target_properties(_sum PROPERTIES SUFFIX ".pyd")
endif()

