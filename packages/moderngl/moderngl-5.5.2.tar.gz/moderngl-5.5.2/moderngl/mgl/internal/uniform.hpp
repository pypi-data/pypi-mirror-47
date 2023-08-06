#pragma once
#include "python.hpp"

#include "opengl/gl_methods.hpp"

PyObject * getset_uniform(const GLMethods & gl, int program_obj, PyObject * uniform, PyObject * value);
PyObject * get_uniforms(const GLMethods & gl, int program_obj);
PyObject * get_attributes(const GLMethods & gl, int program_obj);
