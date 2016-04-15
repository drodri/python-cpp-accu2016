#include <Python.h>  // FIRST, before any other header!!
#include <vector>
#include <numeric>

static PyObject *
average(PyObject *self, PyObject *args){
    PyObject * listObj; 
    if (! PyArg_ParseTuple( args, "O!", &PyList_Type, &listObj))
        return NULL;
     
    std::vector<double> v;
    size_t v_size=PyList_Size(listObj);
    v.reserve(v_size);
    for(size_t i=0;i<v_size;i++){
        PyObject* number = PyList_GetItem(listObj, i); //Borrowed reference.
        v.push_back(PyFloat_AsDouble(number));
    }
    double avg = std::accumulate(v.begin(), v.end(), 0.0) / v_size;
    return Py_BuildValue("d", avg);
}

static PyMethodDef MyMethods[] = {
    {"average",  average, METH_VARARGS, "Average of list floats"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initmymath(void){ // This NAME is COMPULSORY
    (void) Py_InitModule3("mymath", MyMethods,
                          "My documentation of the mymath module");
}
