#include <Python.h>
#include <sstream>

static PyObject *my_callback = NULL;


static PyObject *
module_function(PyObject *self, PyObject *args){
    float a, b, c;

    if (!PyArg_ParseTuple(args, "ff", &a, &b))
        return NULL;
    printf("Binary sum\n");

    c = a + b;
    /* Time to call the callback */
    PyObject* arglist = Py_BuildValue("s", "Adding numbers");
    PyObject* pArgs = PyTuple_New(1); // NOTE: I need a tuple!
    PyTuple_SetItem(pArgs, 0, arglist);
    PyObject* result = PyObject_CallObject(my_callback, pArgs);
    if (result == NULL){
          PyObject* pTypeObj = NULL;
                    PyObject* pValueObj = NULL;
                    PyObject* pWhatObj = NULL;
                    PyErr_Fetch(&pTypeObj, &pValueObj, &pWhatObj);
         printf("Error: %s\n", PyBytes_AsString(pValueObj));
         return NULL; /* Pass error back */
    }

    Py_DECREF(arglist);
    Py_XDECREF(result);
    return Py_BuildValue("f", c);
}


static PyObject *
my_set_callback(PyObject *dummy, PyObject *args)
{
    PyObject *result = NULL;
    PyObject *temp;

    if (PyArg_ParseTuple(args, "O:set_callback", &temp)) {
        if (!PyCallable_Check(temp)) {
            PyErr_SetString(PyExc_TypeError, "parameter must be callable");
            return NULL;
        }
        Py_XINCREF(temp);         /* Add a reference to new callback */
        Py_XDECREF(my_callback);  /* Dispose of previous callback */
        printf("Setting new callback\n");
        my_callback = temp;       /* Remember new callback */
        /* Boilerplate to return "None" */
        Py_INCREF(Py_None);
        result = Py_None;
    }
    return result;
}


static PyMethodDef MyMethods[] = {
    {"add",  module_function, METH_VARARGS, "Adds two numbers"},
    {"reg_log",  my_set_callback, METH_VARARGS, "Registers the logging callback"},
    {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC
initmymath(void){ // This NAME is COMPULSORY
    (void) Py_InitModule("mymath", MyMethods);
}

int
main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);  /* optional but recommended */
    Py_SetPythonHome(".");
    Py_Initialize();
    initmymath();

    PyObject* pName = PyString_FromString("__main__");
    PyObject* pModule = PyImport_Import(pName);
    Py_DECREF(pName);
    PyRun_SimpleString("import mymath\n");
    PyRun_SimpleString("def simple_log(msg):\n    print 'Log ', msg\n"
                       "mymath.reg_log(simple_log)\n");
    PyRun_SimpleString("def suma(a, b):\n    return mymath.add(a, b)\n");

    /*PyRun_SimpleString("print 'Hello World'");
    PyRun_SimpleString("print 'Hello World'");
    std::ostringstream os;
    os<<"a=3\nb=2\nprint suma(a, b)\n";
    PyRun_SimpleString(os.str().c_str());*/

    PyObject* pFunc = PyObject_GetAttrString(pModule, "suma");
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