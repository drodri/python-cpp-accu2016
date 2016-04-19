#include <pybind11/pybind11.h>
#include "zlib.h"

int add(int i, int j) {
    return i + j;
}

namespace py = pybind11;

PYBIND11_PLUGIN(myzlib) {
    py::module m("myzlib", "pybind11 example plugin");

    m.def("sum", &add, "A function which adds two numbers");

    py::class_<z_stream>(m, "z_stream")
        .def(py::init<>())
        .def_readwrite((const char*)"next_in", &z_stream::next_in)
        .def_readwrite("avail_in", &z_stream::avail_in)
        //.def_readwrite("total_in", &z_stream::total_in)
        //.def_readonly("next_out", &z_stream::next_out)
        //.def_readwrite("avail_out", &z_stream::avail_out)
        //.def_readwrite("total_out", &z_stream::total_out)
        //.def_readonly("msg", &z_stream::msg)
        //.def_readonly("state", &z_stream::state)
        //.def_readonly("zalloc", &z_stream::zalloc)
        //.def_readonly("zfree", &z_stream::zfree)
        //.def_readonly("opaque", &z_stream::opaque)
        //.def_readwrite("data_type", &z_stream::data_type)
        //.def_readwrite("adler", &z_stream::adler)
        //.def_readwrite("reserved", &z_stream::reserved)
        ;
     
    return m.ptr();
}