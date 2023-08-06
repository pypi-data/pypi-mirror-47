#include "mgl.hpp"
#include "extensions.hpp"

#include "buffer.hpp"
#include "compute_shader.hpp"
#include "context.hpp"
#include "framebuffer.hpp"
#include "limits.hpp"
#include "program.hpp"
#include "query.hpp"
#include "recorder.hpp"
#include "renderbuffer.hpp"
#include "sampler.hpp"
#include "scope.hpp"
#include "texture.hpp"
#include "vertex_array.hpp"

// TODO: remove
#include "refholder.hpp"

#include "internal/wrapper.hpp"
#include "internal/data_type.hpp"

/* moderngl.core.glprocs(context)
 */
PyObject * meth_glprocs(PyObject * self, PyObject * context) {
    if (!Context_Check(context)) {
        // TODO: error
        return 0;
    }

    MGLContext * ctx = (MGLContext *)get_slot(context, "mglo");
    return PyMemoryView_FromMemory((char *)&ctx->gl, sizeof(ctx->gl), PyBUF_WRITE);
}

void unchain_object(MGLContextObject * mglo, PyObject * obj) {
    set_slot(obj, "mglo", new_ref(Py_None));
    mglo->chain.prev->chain.next = mglo->chain.next;
    mglo->chain.next->chain.prev = mglo->chain.prev;
    mglo->wrapper = NULL;
}

/* moderngl.core.release(obj)
 */
PyObject * meth_release(PyObject * self, PyObject * obj) {
    obj = get_new_wrapper(obj);

    if (Context_Check(obj)) {
        Py_RETURN_NONE;
    }

    if (Buffer_Check(obj)) {
        MGLBuffer * mglo = (MGLBuffer *)new_ref(get_slot(obj, "mglo"));
        unchain_object(mglo, obj);
        mglo->context->gl.DeleteBuffers(1, (unsigned *)&mglo->buffer_obj);
        mglo->buffer_obj = 0;
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    if (ComputeShader_Check(obj)) {
        MGLComputeShader * mglo = (MGLComputeShader *)new_ref(get_slot(obj, "mglo"));
        unchain_object(mglo, obj);
        mglo->context->gl.DeleteProgram(mglo->program_obj);
        mglo->program_obj = 0;
        mglo->context->gl.DeleteShader(mglo->shader_obj);
        mglo->shader_obj = 0;
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    if (Framebuffer_Check(obj)) {
        MGLFramebuffer * mglo = (MGLFramebuffer *)new_ref(get_slot(obj, "mglo"));
        if (mglo == mglo->context->default_framebuffer) {
            PyErr_Format(moderngl_error, "releasing the default framebuffer");
            return NULL;
        }
        unchain_object(mglo, obj);
        mglo->context->gl.DeleteFramebuffers(1, (unsigned *)&mglo->framebuffer_obj);
        mglo->framebuffer_obj = 0;
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    if (Program_Check(obj)) {
        MGLProgram * mglo = (MGLProgram *)new_ref(get_slot(obj, "mglo"));
        unchain_object(mglo, obj);
        mglo->context->gl.DeleteProgram(mglo->program_obj);
        mglo->program_obj = 0;
        for (int i = 0; i < 5; ++i) {
            mglo->context->gl.DeleteShader(mglo->shader_obj[i]);
            mglo->shader_obj[i] = 0;
        }
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    if (Query_Check(obj)) {
        MGLQuery * mglo = (MGLQuery *)new_ref(get_slot(obj, "mglo"));
        unchain_object(mglo, obj);
        for (int i = 0; i < 4; ++i) {
            if (mglo->query_obj[i]) {
                mglo->context->gl.DeleteQueries(1, (unsigned *)&mglo->query_obj[i]);
                mglo->query_obj[i] = 0;
            }
        }
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    if (Renderbuffer_Check(obj)) {
        MGLRenderbuffer * mglo = (MGLRenderbuffer *)new_ref(get_slot(obj, "mglo"));
        unchain_object(mglo, obj);
        mglo->context->gl.DeleteRenderbuffers(1, (unsigned *)&mglo->renderbuffer_obj);
        mglo->renderbuffer_obj = 0;
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    if (Sampler_Check(obj)) {
        MGLSampler * mglo = (MGLSampler *)new_ref(get_slot(obj, "mglo"));
        unchain_object(mglo, obj);
        mglo->context->gl.DeleteSamplers(1, (unsigned *)&mglo->sampler_obj);
        mglo->sampler_obj = 0;
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    if (Scope_Check(obj)) {
        MGLScope * mglo = (MGLScope *)new_ref(get_slot(obj, "mglo"));
        if (mglo == mglo->context->default_scope) {
            PyErr_Format(moderngl_error, "releasing the default scope");
            return NULL;
        }
        unchain_object(mglo, obj);
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    if (Texture_Check(obj)) {
        MGLTexture * mglo = (MGLTexture *)new_ref(get_slot(obj, "mglo"));
        if (obj != mglo->wrapper) {
            PyErr_Format(moderngl_error, "releasing texture levels or layers");
            return NULL;
        }
        unchain_object(mglo, obj);
        mglo->context->gl.DeleteTextures(1, (unsigned *)&mglo->texture_obj);
        mglo->texture_obj = 0;
        Py_DECREF(obj);
        Py_DECREF(mglo);
        Py_RETURN_NONE;
    }

    PyErr_BadInternalCall();
    return 0;
}

fastcallable(meth_create_context)

PyMethodDef module_methods[] = {
    {"create_context", fastcall(meth_create_context), fastcall_flags, NULL},
    {"extensions", (PyCFunction)meth_extensions, METH_O, 0},
    {"hwinfo", (PyCFunction)meth_hwinfo, METH_O, 0},
    // {"inspect", (PyCFunction)meth_inspect, METH_O, 0},
    {"glprocs", (PyCFunction)meth_glprocs, METH_O, 0},
    {"release", (PyCFunction)meth_release, METH_O, 0},

    {"extend_context", (PyCFunction)meth_extend_context, METH_VARARGS, 0},
    {"extend_buffer", (PyCFunction)meth_extend_buffer, METH_VARARGS, 0},
    {"extend_framebuffer", (PyCFunction)meth_extend_framebuffer, METH_VARARGS, 0},
    {"extend_program", (PyCFunction)meth_extend_program, METH_VARARGS, 0},
    {"extend_renderbuffer", (PyCFunction)meth_extend_renderbuffer, METH_VARARGS, 0},
    {"extend_texture", (PyCFunction)meth_extend_texture, METH_VARARGS, 0},
    {"extend_refholder", (PyCFunction)meth_extend_refholder, METH_VARARGS, 0},
    {0},
};

/* Module definition */

PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "moderngl.mgl.new", 0, -1, module_methods, 0, 0, 0, 0};

inline PyTypeObject * _new_type(PyObject * module, const char * name, PyType_Spec * spec) {
    PyObject * type = must_have(PyType_FromSpec(spec));
    PyModule_AddObject(module, name, new_ref(type));
    return (PyTypeObject *)type;
};

#define new_type(name) name ## _class = _new_type(module, #name, &name ## _spec)

PyObject * PyInit_mgl_new() {
    PyObject * module = PyModule_Create(&module_def);

    interns = PyList_New(0);
    PyModule_AddObject(module, "interns", interns);

    new_type(MGLBuffer);
    new_type(MGLComputeShader);
    new_type(MGLContext);
    new_type(MGLFramebuffer);
    new_type(MGLProgram);
    new_type(MGLQuery);
    new_type(MGLRecorder);
    new_type(MGLRenderbuffer);
    new_type(MGLSampler);
    new_type(MGLScope);
    new_type(MGLTexture);
    new_type(MGLVertexArray);

    // TODO: remove
    new_type(MGLRefholder);

    f1.numpy_dtype = intern(PyUnicode_FromString("f1"));
    f2.numpy_dtype = intern(PyUnicode_FromString("f2"));
    f4.numpy_dtype = intern(PyUnicode_FromString("f4"));
    u1.numpy_dtype = intern(PyUnicode_FromString("u1"));
    u2.numpy_dtype = intern(PyUnicode_FromString("u2"));
    u4.numpy_dtype = intern(PyUnicode_FromString("u4"));
    i1.numpy_dtype = intern(PyUnicode_FromString("i1"));
    i2.numpy_dtype = intern(PyUnicode_FromString("i2"));
    i4.numpy_dtype = intern(PyUnicode_FromString("i4"));

    return module;
}
