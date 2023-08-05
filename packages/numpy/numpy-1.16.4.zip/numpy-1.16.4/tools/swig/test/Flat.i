// -*- c++ -*-
%module Flat

%{
#define SWIG_FILE_WITH_INIT
#include "Flat.h"
%}

// Get the NumPy typemaps
%include "../numpy.i"

%init %{
  import_array();
%}

%define %apply_numpy_typemaps(TYPE)

%apply (TYPE* INPLACE_ARRAY_FLAT, int DIM_FLAT) {(TYPE* array, int size)};

%enddef    /* %apply_numpy_typemaps() macro */

%apply_numpy_typemaps(signed char       )
%apply_numpy_typemaps(unsigned char     )
%apply_numpy_typemaps(short             )
%apply_numpy_typemaps(unsigned short    )
%apply_numpy_typemaps(int               )
%apply_numpy_typemaps(unsigned int      )
%apply_numpy_typemaps(long              )
%apply_numpy_typemaps(unsigned long     )
%apply_numpy_typemaps(long long         )
%apply_numpy_typemaps(unsigned long long)
%apply_numpy_typemaps(float             )
%apply_numpy_typemaps(double            )

// Include the header file to be wrapped
%include "Flat.h"
