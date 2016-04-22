#include <Python.h>
#include <vector>
#include <numeric>

static PyObject *
average(PyObject *self, PyObject *args){
    PyObject * listObj; 
    if (! PyArg_ParseTuple( args, "O!",
                &PyList_Type, &listObj))
        return NULL;
    
    std::vector<double> v;
    auto v_size=PyList_Size(listObj);
    v.reserve(v_size);
    for(auto i=0;i<v_size;i++){
        auto number = PyList_GetItem(listObj, i); //Borrowed reference.
        v.push_back(PyFloat_AsDouble(number));
    }
    auto avg = std::accumulate(v.begin(), v.end(), 0.0) / v_size;
    return Py_BuildValue("d", avg);
}

static PyMethodDef MyMethods[] = {
    {"average",  average, METH_VARARGS, "Average of list floats"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initmymath(void){
    (void) Py_InitModule3("mymath", MyMethods,
                          "My documentation of the mymath module");
}
