#include <pybind11/pybind11.h>
#include "Poco/Random.h"

using Poco::Random;

namespace py = pybind11;

PYBIND11_PLUGIN(pypoco) {
    py::module m("pypoco", "pybind11 example plugin");

    py::class_<Random>(m, "Random")
        .def(py::init<>())
        .def("nextFloat", &Random::nextFloat);
     
    return m.ptr();
}