#pragma once
#include "python.hpp"

struct MGLDataType {
    PyObject * numpy_dtype;
    int base_format[5];
    int internal_format[5];
    int gl_type;
    int size;
    char shape;
};

extern MGLDataType f1;
extern MGLDataType f2;
extern MGLDataType f4;
extern MGLDataType u1;
extern MGLDataType u2;
extern MGLDataType u4;
extern MGLDataType i1;
extern MGLDataType i2;
extern MGLDataType i4;
extern MGLDataType d2;
extern MGLDataType d3;
extern MGLDataType d4;

MGLDataType * from_dtype(PyObject * dtype);
