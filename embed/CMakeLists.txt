project(MyApp)
set (CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_BINARY_DIR})

include_directories("C:\Python27\include")
link_directories("C:\Python27\libs")
add_executable(app main.cpp)
target_link_libraries(app python27)
