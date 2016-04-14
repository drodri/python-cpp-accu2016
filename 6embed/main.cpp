#include <Python.h>
#include <sstream>

int
main(int argc, char *argv[])
{
    Py_SetProgramName(argv[0]);
    Py_SetPythonHome(".");
    Py_Initialize();

    PyRun_SimpleString("print 'Hello World'");
    
    Py_Finalize();
    return 0;
}

/*  std::ostringstream os;
    os<<"a=3\nb=2\nprint a, b\n";
    PyRun_SimpleString(os.str().c_str());
*/