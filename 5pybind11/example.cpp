#include <pybind11/pybind11.h>
#include <vector>
#include <numeric>
#include <pybind11/stl.h>
#include <pybind11/operators.h>

/*int add(int i, int j) {
    return i + j;
}

namespace py = pybind11;

PYBIND11_PLUGIN(example) {
    py::module m("example", "pybind11 example plugin");

    m.def("sum", &add, "A function which adds two numbers");

    return m.ptr();
}*/

int add(int i, int j) {
    return i + j;
}
struct Data{
    Data(float t): value(t){}
    Data operator*(float factor) const { return Data(value * factor); }
    float value;
};

struct ZStream{
    char* input;
};

float avg(const std::vector<float>& v){
    auto acc = std::accumulate(v.begin(), v.end(), 0.0f);
    return acc/v.size();
}

float avg(const std::vector<Data>& v){
    auto acc = std::accumulate(v.begin(), v.end(), 0.0f,
                               [](float a, const Data& obj)
                               {return a + obj.value;});
    return acc/v.size();
}

float mydup(float* value){
    return *value * 2;
}
namespace py = pybind11;

PYBIND11_PLUGIN(example) {
    py::module m("example", "pybind11 example plugin");
    
    py::class_<Data>(m, "Data")
        .def(py::init<float>())
        .def(py::self * float())
        .def_readwrite("value", &Data::value)
        ;
        
    py::class_<ZStream>(m, "ZStream")
        .def(py::init<>())
        .def_readwrite("input", &ZStream::input)
        ;
        
    m.def("sum", &add, "A function which adds two numbers");
    m.def("avg", (float (*)(const std::vector<float>& v)) &avg, "Average of vector");
    m.def("avg", (float (*)(const std::vector<Data>& v)) &avg, "Average of vector");
    m.def("mydup",  &mydup, "Duplicate");

    return m.ptr();
}