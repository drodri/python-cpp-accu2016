#include <Python.h>
#include <iostream>

static PyObject *
module_function(PyObject *self, PyObject *args){
    float a, b, c;
    if (!PyArg_ParseTuple(args, "ff", &a, &b))
        return NULL;
    c = a + b;
    return Py_BuildValue("f", c);
}

static PyMethodDef MyMethods[] = {
    {"add",  module_function, METH_VARARGS, "Adds two numbers"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initmymath(void){ // This NAME is COMPULSORY
    (void) Py_InitModule("mymath", MyMethods);
}

int main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);
    Py_SetPythonHome("C:/Python27");
    Py_Initialize();
    initmymath(); //REMEMBER!!

    PyObject* pName = PyString_FromString("__main__");
    PyObject* pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    
    PyRun_SimpleString("import mymath");
    PyRun_SimpleString("def add(a, b):\n    return mymath.add(a, b)\n");

    PyObject* pFunc = PyObject_GetAttrString(pModule, "add");
    PyObject* pArgs = PyTuple_New(2);
    PyObject* param1 = PyFloat_FromDouble(2.1);
    PyTuple_SetItem(pArgs, 0, param1);
    PyObject* param2 = PyFloat_FromDouble(3.2);
    PyTuple_SetItem(pArgs, 1, param2);

    PyObject* pValue = PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pArgs);

    printf("Result of call: %lf\n", PyFloat_AsDouble(pValue));
    Py_DECREF(pValue);
    
    Py_Finalize();
    return 0;
}

