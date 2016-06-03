#include <Python.h>  // FIRST, before any other header!!
#include <stdlib.h>

static PyObject *my_callback = NULL;

static PyObject *
call_log(const char* msg){
    PyObject* arglist = Py_BuildValue("s", msg);
    PyObject* pArgs = PyTuple_New(1); // NOTE: I need a tuple!
    PyTuple_SetItem(pArgs, 0, arglist);
    PyObject* result = PyObject_CallObject(my_callback, pArgs);
    if (result == NULL)
         return NULL; /* Pass error back */
    Py_DECREF(pArgs);
    Py_DECREF(arglist);
    Py_XDECREF(result);
    Py_RETURN_NONE; //INCREF, then return
}

static PyObject *
set_callback(PyObject *dummy, PyObject *args){
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);       
        Py_XDECREF(my_callback);
        my_callback = temp;   

        //Py_RETURN_NONE 
        Py_INCREF(Py_None);
        result = Py_None;
    }
    return result;
}

static PyObject *
module_function(PyObject *self, PyObject *args){
    float a, b, c;
    if (!PyArg_ParseTuple(args, "ff", &a, &b))
        return NULL;
    c = a + b;
    call_log("Adding 2 numbers");
    return Py_BuildValue("f", c);
}

static PyMethodDef MyMethods[] = {
    {"add",  module_function, METH_VARARGS, "Adds two numbers"},
    {"reg_log",  set_callback, METH_VARARGS, "Registers the logging callback"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initmymath(void){ // This NAME is COMPULSORY
    (void) Py_InitModule3("mymath", MyMethods,
                          "My documentation of the mymath module");
}

//"C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin\dumpbin.exe" /EXPORTS mymath.pyd