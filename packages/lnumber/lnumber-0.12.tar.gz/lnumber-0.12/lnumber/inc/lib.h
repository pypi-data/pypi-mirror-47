#pragma once

#if defined(_MSC_VER) && defined(_WIN32)
  #ifdef LIBLNUMBER_EXPORTS
    #define LIBLNUMBER_LIBRARY_INTERFACE __declspec(dllexport)
  #else
    #define LIBLNUMBER_LIBRARY_INTERFACE __declspec(dllimport)
  #endif
#else
  #define LIBLNUMBER_LIBRARY_INTERFACE
  #include <cstddef>
#endif

extern "C"
{ //stops MSVC from mangling
  size_t LIBLNUMBER_LIBRARY_INTERFACE laman_number(char* graph, size_t verts);
}
