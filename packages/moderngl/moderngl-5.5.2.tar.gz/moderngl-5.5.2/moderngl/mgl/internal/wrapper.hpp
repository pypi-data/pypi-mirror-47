#pragma once

#include "python.hpp"
#include "intern.hpp"

#define Attribute_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Attribute_class)
#define Buffer_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Buffer_class)
#define ComputeShader_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)ComputeShader_class)
#define Context_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Context_class)
#define Framebuffer_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Framebuffer_class)
#define Limits_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Limits_class)
#define Program_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Program_class)
#define Query_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Query_class)
#define Renderbuffer_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Renderbuffer_class)
#define Sampler_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Sampler_class)
#define Scope_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Scope_class)
#define Texture_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Texture_class)
#define Uniform_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)Uniform_class)
#define VertexArray_Check(obj) (Py_TYPE(obj) == (PyTypeObject *)VertexArray_class)

#define Attribute_New(...) must_have(PyObject_CallFunction(Attribute_class, __VA_ARGS__))
#define Buffer_New(...) must_have(PyObject_CallFunction(Buffer_class, __VA_ARGS__))
#define ComputeShader_New(...) must_have(PyObject_CallFunction(ComputeShader_class, __VA_ARGS__))
#define Context_New(...) must_have(PyObject_CallFunction(Context_class, __VA_ARGS__))
#define Framebuffer_New(...) must_have(PyObject_CallFunction(Framebuffer_class, __VA_ARGS__))
#define Limits_New(...) must_have(PyObject_CallFunction(Limits_class, __VA_ARGS__))
#define Program_New(...) must_have(PyObject_CallFunction(Program_class, __VA_ARGS__))
#define Query_New(...) must_have(PyObject_CallFunction(Query_class, __VA_ARGS__))
#define Renderbuffer_New(...) must_have(PyObject_CallFunction(Renderbuffer_class, __VA_ARGS__))
#define Sampler_New(...) must_have(PyObject_CallFunction(Sampler_class, __VA_ARGS__))
#define Scope_New(...) must_have(PyObject_CallFunction(Scope_class, __VA_ARGS__))
#define Texture_New(...) must_have(PyObject_CallFunction(Texture_class, __VA_ARGS__))
#define Uniform_New(...) must_have(PyObject_CallFunction(Uniform_class, __VA_ARGS__))
#define VertexArray_New(...) must_have(PyObject_CallFunction(VertexArray_class, __VA_ARGS__))

// TODO: remove
#define Refholder_New(...) must_have(PyObject_CallFunction(Refholder_class, __VA_ARGS__))
