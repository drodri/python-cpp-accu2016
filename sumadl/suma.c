#include "suma.h"
#include <stdio.h>


float suma(float a, float b){
    printf("Adding %f + %f", a, b);
    float c = a + b;
    printf("Result %f", c);
    return c;
}