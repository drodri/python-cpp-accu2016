#pragma once

#ifdef WIN32
  #define DLL_EXPORT __declspec(dllexport)
#else
  #define DLL_EXPORT
#endif

DLL_EXPORT float sum(float a, float b);