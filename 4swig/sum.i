/* sum.i */
%module sum
 %{
 /* Includes the header in the wrapper code */
  #include "sum.h"
 %}
 
 /* Parse the header file to generate wrappers */
 %include "sum.h"