#include <Python.h>
#include <iostream>

int
main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);
    Py_SetPythonHome("C:/Python27");
    Py_Initialize();

    PyObject* pName = PyString_FromString("__main__");
    PyObject* pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    
    PyRun_SimpleString("def add(a, b):\n    return a+b\n");

    PyObject* pFunc = PyObject_GetAttrString(pModule, "add");
    PyObject* pArgs = PyTuple_New(2);
    PyObject* param1 = PyFloat_FromDouble(2.1);
    Py_INCREF(param1); //Note this incr if we want to use after tuple
    PyTuple_SetItem(pArgs, 0, param1);
    PyObject* param2 = PyFloat_FromDouble(3.2);
    PyTuple_SetItem(pArgs, 1, param2);

    PyObject* pValue = PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pArgs);

    printf("Result of call: %lf\n", PyFloat_AsDouble(pValue));
    Py_DECREF(pValue);
    
    double d = PyFloat_AsDouble(param1);
    std::cout<<d<<std::endl;
    
    Py_Finalize();
    return 0;
}

