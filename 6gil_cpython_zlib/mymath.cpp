
#include <Python.h>  // FIRST, before any other header!!
#include "zlib.h"

static PyObject *
deflate(PyObject *self, PyObject *args){
    char* str;
    if (!PyArg_ParseTuple(args, "s", &str))
        return NULL;
    
    size_t size = strlen(str)+1;
    char* b = new char[size];
    z_stream defstream;
    defstream.zalloc = Z_NULL;
    defstream.zfree = Z_NULL;
    defstream.opaque = Z_NULL;
    defstream.avail_in = (uInt)size; // size of input, string + terminator
    defstream.next_in = (Bytef *)str; // input char array
    defstream.avail_out = (uInt)size; // size of output
    defstream.next_out = (Bytef *)b; // output char array
    
    // the actual compression work.
    Py_BEGIN_ALLOW_THREADS 
    
    deflateInit(&defstream, Z_BEST_COMPRESSION);
    deflate(&defstream, Z_FINISH);
    deflateEnd(&defstream);
    
    Py_END_ALLOW_THREADS
   
    PyObject * result = Py_BuildValue("s#", b, defstream.total_out);
    delete [] b;
    return result;
}

static PyObject *
inflate(PyObject *self, PyObject *args){
    const char* str;
    char * buf;
    Py_ssize_t count;
    if (!PyArg_ParseTuple(args, "s#", &str, &count))
        return NULL;
     
    char* b = new char[2400000]; //FIXME, FIXME
    
    z_stream infstream;
    infstream.zalloc = Z_NULL;
    infstream.zfree = Z_NULL;
    infstream.opaque = Z_NULL;
    infstream.avail_in = (uInt)count; // size of input
    infstream.next_in = (Bytef *)str; // input char array
    infstream.avail_out = (uInt)2400000; // size of output
    infstream.next_out = (Bytef *)b; // output char array
    
    Py_BEGIN_ALLOW_THREADS
    
    inflateInit(&infstream);
    inflate(&infstream, Z_NO_FLUSH);
    inflateEnd(&infstream);
    
    Py_END_ALLOW_THREADS
   
    PyObject * result = Py_BuildValue("s", b);
    delete [] b;
    return result;
}

static PyMethodDef MyMethods[] = {
    {"deflate",  deflate, METH_VARARGS, "compress data"},
    {"inflate",  inflate, METH_VARARGS, "decompress data"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initmymath(void){ // This NAME is COMPULSORY
    (void) Py_InitModule3("mymath", MyMethods,
                          "My documentation of the mymath module");
}
