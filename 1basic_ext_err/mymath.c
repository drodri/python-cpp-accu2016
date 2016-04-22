#include <Python.h>
static PyObject* MyMathError;

static PyObject* divide(PyObject *self, PyObject *args){
    int a, b, c;
    if (!PyArg_ParseTuple(args, "ii", &a, &b)){
        PyObject* err=PyErr_Occurred();
        PyErr_SetString(err, "Bad param!!");
        return NULL;
    }
    if(a==0 && b==0){
        PyErr_SetString(MyMathError,"Undefined value 0/0");
        return NULL;
    }
    if(b==0){
        PyErr_SetString(PyExc_ZeroDivisionError,"Division by 0");
        //Py_RETURN_NONE; => Nothing happens, no py exception raised
        return NULL; 
    }
    c = a/b;
    return Py_BuildValue("i", c);
}

static PyMethodDef MyMethods[] = {
    {"divide",  divide, METH_VARARGS, "Divide two numbers"},
    {NULL, NULL, 0, NULL}       
};

PyMODINIT_FUNC initmymath(void){
    PyObject* m = Py_InitModule3("mymath", MyMethods,
                          "My documentation of the mymath module");
    MyMathError = PyErr_NewException("mymath.MathError", NULL, NULL);
    Py_INCREF(MyMathError); //IMPORTANT!
    PyModule_AddObject(m, "MathError", MyMathError);
}