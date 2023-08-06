#pragma once
#include "context.hpp"

struct MGLBuffer : public MGLContextObject {
    int buffer_obj;
    int flags;
    Py_ssize_t size;
};

extern PyType_Spec MGLBuffer_spec;
extern PyTypeObject * MGLBuffer_class;

PyObject * MGLContext_meth_buffer(MGLContext * self, PyObject * const * args, Py_ssize_t nargs);
PyObject * MGLContext_meth_copy_buffer(MGLContext * self, PyObject * const * args, Py_ssize_t nargs);

const int MGL_BUFFER_READABLE = 0x0001;
const int MGL_BUFFER_WRITABLE = 0x0002;
const int MGL_BUFFER_IMMUTABLE = 0x0004;
const int MGL_BUFFER_LOCAL = 0x0008;
const int MGL_BUFFER_OPEN = 0x0400;
const int MGL_BUFFER_READING = 0x0100 | MGL_BUFFER_OPEN;
const int MGL_BUFFER_WRITING = 0x0200 | MGL_BUFFER_OPEN;

#define OPEN_ERROR(flags) (flags & MGL_BUFFER_OPEN)
#define READ_ERROR(flags) (!(flags & MGL_BUFFER_READABLE))
#define WRITE_ERROR(flags) (!(flags & MGL_BUFFER_WRITABLE))
#define RANGE_ERROR(offset, size, limit) (offset < 0) || (offset + size > limit)
#define DTYPE_ERROR(dtype) (dtype != Py_None && numpy_frombuffer == 0)
