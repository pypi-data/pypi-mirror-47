#include "extensions.hpp"
#include "context.hpp"

#include "internal/wrapper.hpp"

/* moderngl.core.extensions(context)
 * Returns a list of supported extensions.
 */
PyObject * meth_extensions(PyObject * self, PyObject * context) {
    context = get_new_wrapper(context);

    if (!Context_Check(context)) {
        // TODO: error
        return 0;
    }

    MGLContext * ctx = (MGLContext *)get_slot(context, "mglo");
    int version_code = PyLong_AsLong(get_slot(context, "version_code"));
    const GLMethods & gl = ctx->gl;

    if (version_code >= 300) {
        int num_extensions = 0;
        gl.GetIntegerv(GL_NUM_EXTENSIONS, &num_extensions);
        PyObject * lst = PyList_New(num_extensions);
        for (int i = 0; i < num_extensions; ++i) {
            const char * ext = (const char *)gl.GetStringi(GL_EXTENSIONS, i);
            PyList_SET_ITEM(lst, i, PyUnicode_FromString(ext));
        }
        return lst;
    } else {
        const char * ext = (const char *)gl.GetString(GL_EXTENSIONS);
        if (!ext) {
            return PyList_New(0);
        }
        PyObject * extensions = PyUnicode_FromString(ext);
        PyObject * lst = PyUnicode_Split(extensions, 0, -1);
        Py_DECREF(extensions);
        return lst;
    }
}

/* moderngl.core.hwinfo(context)
 */
PyObject * meth_hwinfo(PyObject * self, PyObject * context) {
    context = get_new_wrapper(context);

    if (!Context_Check(context)) {
        // TODO: error
        return 0;
    }

    MGLContext * ctx = (MGLContext *)get_slot(context, "mglo");
    const GLMethods & gl = ctx->gl;

    const char * version = (const char *)gl.GetString(GL_VERSION);
    const char * vendor = (const char *)gl.GetString(GL_VENDOR);
    const char * renderer = (const char *)gl.GetString(GL_RENDERER);
    const char * glsl = (const char *)gl.GetString(GL_SHADING_LANGUAGE_VERSION);

    PyObject * version_str = PyUnicode_FromString(version ? version : "");
    PyObject * vendor_str = PyUnicode_FromString(vendor ? vendor : "");
    PyObject * renderer_str = PyUnicode_FromString(renderer ? renderer : "");
    PyObject * glsl_str = PyUnicode_FromString(glsl ? glsl : "");

    PyObject * res = PyDict_New();
    PyDict_SetItemString(res, "version", version_str);
    PyDict_SetItemString(res, "vendor", vendor_str);
    PyDict_SetItemString(res, "renderer", renderer_str);
    PyDict_SetItemString(res, "glsl", glsl_str);
    return res;
}
