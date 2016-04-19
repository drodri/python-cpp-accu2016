#include <Python.h>
#include <iostream>

static PyObject *my_callback = NULL;

static PyObject *
set_callback(PyObject *dummy, PyObject *args)
{
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
    PyObject* arglist = Py_BuildValue("s", "Adding numbers");
    PyObject* pArgs = PyTuple_New(1); // NOTE: I need a tuple!
    PyTuple_SetItem(pArgs, 0, arglist);
    PyObject* result = PyObject_CallObject(my_callback, pArgs);
    if (result == NULL){
          PyObject* pTypeObj = NULL;
            PyObject* pValueObj = NULL;
            PyObject* pWhatObj = NULL;
            PyErr_Fetch(&pTypeObj, &pValueObj, &pWhatObj);
         printf("Error callback: %s\n", PyBytes_AsString(pValueObj));
         return NULL; /* Pass error back */
    }

    Py_DECREF(arglist);
    Py_XDECREF(result);
    return Py_BuildValue("f", c);
}

static PyMethodDef MyMethods[] = {
    {"add",  module_function, METH_VARARGS, "Adds two numbers"},
    {"reg_log",  set_callback, METH_VARARGS, "Registers the logging callback"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initmymath(void){
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
    PyRun_SimpleString("def simple_log(msg):\n    print 'Log ', msg2\n\n"
                       "mymath.reg_log(simple_log)\n");
    PyRun_SimpleString("def add(a, b):\n    return mymath.add(a, b)\n");

    PyObject* pFunc = PyObject_GetAttrString(pModule, "add");
    PyObject* pArgs = PyTuple_New(2);
    PyObject* param1 = PyFloat_FromDouble(2.1);
    PyTuple_SetItem(pArgs, 0, param1);
    PyObject* param2 = PyFloat_FromDouble(3.2);
    PyTuple_SetItem(pArgs, 1, param2);

    PyObject* pValue = PyObject_CallObject(pFunc, pArgs);
    Py_DECREF(pArgs);
    if(pValue==NULL)
        printf("Call failed\n");
    else{
        printf("Result of call: %lf\n", PyFloat_AsDouble(pValue));
        Py_XDECREF(pValue);  
    }
        
    Py_Finalize();
    return 0;
}

