#include <Python.h>  // FIRST, before any other header!!
#include <time.h>
#include <stdlib.h>

static PyObject *
module_function(PyObject *self, PyObject *args){
    float a, b, c;

    if (!PyArg_ParseTuple(args, "ff", &a, &b))
        return NULL;

    c = a + b;
    return Py_BuildValue("f", c);
}

static PyObject *
myrandom(PyObject *self, PyObject *args){
    int r = rand();
    float a = r/(float)RAND_MAX;
    return Py_BuildValue("f", a);
}

static PyMethodDef MyMethods[] = {
    {"add",  module_function, METH_VARARGS, "Adds two numbers"},
    {"random",  myrandom, METH_NOARGS, "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initmymath(void) // This NAME is COMPULSORY
{
    srand((int)time(NULL));
    (void) Py_InitModule3("mymath", MyMethods,
                          "My documentation of the mymath module");
}