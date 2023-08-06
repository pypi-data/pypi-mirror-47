#include "internal/python.hpp"

PyObject * get_new_wrapper(PyObject * old_wrapper);

PyObject * meth_extend_context(PyObject * self, PyObject * args);
PyObject * meth_extend_buffer(PyObject * self, PyObject * args);
PyObject * meth_extend_framebuffer(PyObject * self, PyObject * args);
PyObject * meth_extend_program(PyObject * self, PyObject * args);
PyObject * meth_extend_renderbuffer(PyObject * self, PyObject * args);
PyObject * meth_extend_texture(PyObject * self, PyObject * args);
PyObject * meth_extend_refholder(PyObject * self, PyObject * args);
