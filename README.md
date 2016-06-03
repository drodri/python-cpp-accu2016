# Python and C/C++: Python extensions and embedding

Thit is the supporting code for the Accu 2016 (Bristol, UK) conference talk I did, as I like to provide if possible real working examples.

I also did a shorter version of the talk at Sydney (Australia) Python Meetup the 2nd June 2016, just briefly introducing the Python/C API.

The code is just for presenting and introducing concepts, so it may have bugs, can be incomplete, even have bad SW engineering practices.

It was tested/presented in Win10, win VS2015 compiler, but most of the examples should work on other platforms with little effort.

For some examples using third party C or C++ libraries, I am using the [Conan C and C++ package manager](https://conan.io).

## Python/C API examples

You should be able to run them with distutils: ``$ python setup.py install``. Virtualenv recommended, of course.
For the C++ example in Windows, you might need the VS2015 compiler, and set the environment variable to let python
use this compiler: ``$  SET VS90COMNTOOLS=%VS140COMNTOOLS%``

- 1basic_ext. The most basic example of an extension, in C, to add 2 numbers
- 1basic_ext_cpp. Ey, we can use modern C++ too. Average of a list of floats example.
- 1basic_ext_err. How to handle errors in the C code, throw python exceptions, even create your own module exceptions
- 1basic_ext_fcallback. Calling python functions from the C/C++ code: callbacks

## Wrapping shared libs from python

In these examples we have an existing shared lib (DLL in win), that can be built using cmake. These examples use ctypes or cffi
to directly load and use the DLL.

- 2ctypes: Very basic addition of two numbers, using ctypes
- 2ctypes_zlib: an example of compression-decompression using zlib and ctypes
- 3cffi: Example (using exactly the same dll, just copy the dll from the previous example), but using C foreign function interface, CFFI, online, ABI mode
- 3cffi_out: Same as previous but doing offline pre-processing to avoid parsing overhead at import time.
- 3cffi_zlib: a failed attempt to do the same I did with ctypes and zlib. Done some debugging, but still failing.
- 3cffi_zlib_api: same as above but using the API mode. Also failing.

## Extensions with SWIG

An example of a code generation approach. SWIG will generate C code that can be compiled and linked (also with CMake), to easily create an extension.
It uses an IDL (sum.i file) to define the interface of the code to generate. SWIG also generates for other languages.

- 4swig: Basic sum example with SWIG.

## Bulding extensions directly from C++

The reference approach would be Boost.Python, but successor project Pybind11 has a large traction, it is modern, support latest compilers, header only (much easier to use),
good support... so I decided to try it, works great. A very good option for C++ devs.

- 5pybind11: very basic example of an extension with some math functions
- 5pybind11_zlib: another failed attempt to wrap Zlib. In this case, it was basically the very low level of the base structure with raw pointers, that didn't 
  fit well in the (C++) framework. It is possible, but the workarounds a bit tricky, so not finished (doesnt work)
- 5pybind11_poco: example of extension using Pybind and the C++ Poco well known library. 


## Talking about the GIL (I know I shouldn't)

Back to the Python/C API, we went there for performance, so maybe it makes sense to release the GIL if we are in pure C/C++ code (i.e. not using python 
objects at all), doing some heavy computation or IO

- 6gil_cpython: How to release/acquire the GIL again example in the C++ extension of example 1basic_ext_cpp, the average of a list of floats.
- 6gil_cpython_zlib: Wrapping ZLib with the Python/C API might be a bit more verbose than other techniques (ctypes, cffi), but very easy to develop and debug.
  Example of release/acquire the GIL in the compression computation
  
## Embedding the python interpreter in a C or C++ app

Very easy. Add python scripting language for configuration, plugins... to your C/C++ app. All of them are C/C++ apps built with CMake.

- 7embed: Minimal example how to run some string
- 7embed_call: Call a given function inside some text defined to the C/C++ app
- 7embed_extend: Invoke the python interpreter from the C/C++ app, and in turn, let the python code call C/C++ code too (similar to the extensions previously defined,
actually the code is the same)
- 7embed_extend_callback: Invoke the python interpreter from the C/C++ app, which calls to C/C++ code, which also makes another callback to a python function. To infinity and beyond!



