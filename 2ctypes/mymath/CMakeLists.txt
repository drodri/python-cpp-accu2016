project(mymath C)
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE
      ${CMAKE_BINARY_DIR}/../../)

add_library(mymath SHARED sum.c)
# cmake .. -G "Visual Studio 14" && cmake --build . --config Release
