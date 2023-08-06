#include "adaptor.hpp"

#include "internal/python.hpp"
#include "internal/opengl/gl_methods.hpp"
#include "internal/opengl/gl_context.hpp"
#include "internal/wrapper.hpp"
#include "internal/uniform.hpp"
#include "mgl/buffer.hpp"
#include "mgl/context.hpp"
#include "mgl/framebuffer.hpp"
#include "mgl/program.hpp"
#include "mgl/query.hpp"
#include "mgl/renderbuffer.hpp"
#include "mgl/sampler.hpp"
#include "mgl/texture.hpp"
#include "mgl/vertex_array.hpp"
#include "mgl/refholder.hpp"

struct MGLBuffer_old;
struct MGLComputeShader_old;
struct MGLContext_old;
struct MGLFramebuffer_old;
struct MGLProgram_old;
struct MGLQuery_old;
struct MGLRenderbuffer_old;
struct MGLSampler_old;
struct MGLScope_old;
struct MGLTexture_old;
struct MGLTexture3D_old;
struct MGLTextureArray_old;
struct MGLTextureCube_old;
struct MGLVertexArray_old;

struct MGLDataType;

struct MGLBuffer_old {
	PyObject_HEAD

	MGLContext * context;

	int buffer_obj;

	Py_ssize_t size;
	bool dynamic;
};

struct MGLComputeShader_old {
	PyObject_HEAD

	MGLContext * context;

	int program_obj;
	int shader_obj;
};

struct MGLContext_old {
	PyObject_HEAD

	MGLFramebuffer_old * default_framebuffer;
	MGLFramebuffer_old * bound_framebuffer;

	GLContext gl_context;

	int version_code;

	int max_samples;
	int max_integer_samples;
	int max_color_attachments;

	int max_texture_units;
	int default_texture_unit;
	float max_anisotropy;

	int enable_flags;
	int front_face;

	int depth_func;
	int blend_func_src;
	int blend_func_dst;

	bool wireframe;
	bool multisample;

	int provoking_vertex;

	GLMethods gl;
};

struct MGLFramebuffer_old {
	PyObject_HEAD

	MGLContext_old * context;

	bool * color_mask;

	unsigned * draw_buffers;
	int draw_buffers_len;

	int framebuffer_obj;

	int viewport_x;
	int viewport_y;
	int viewport_width;
	int viewport_height;

	int width;
	int height;
	int samples;

	bool depth_mask;
};

struct MGLProgram_old {
	PyObject_HEAD

	MGLContext_old * context;

	int geometry_input;
	int geometry_output;

	int program_obj;

	int num_vertex_shader_subroutines;
	int num_fragment_shader_subroutines;
	int num_geometry_shader_subroutines;
	int num_tess_evaluation_shader_subroutines;
	int num_tess_control_shader_subroutines;

	int geometry_vertices;
	int num_varyings;
};

struct MGLQuery_old {
	PyObject_HEAD

	MGLContext_old * context;

	int query_obj[4];
};

struct MGLRenderbuffer_old {
	PyObject_HEAD

	MGLContext_old * context;
	MGLDataType * data_type;

	union {
		int renderbuffer_obj;
		int texture_obj;
	};

	int width;
	int height;
	int components;

	int samples;
	bool depth;
};

struct MGLSampler_old {
	PyObject_HEAD

	MGLContext_old * context;
	int sampler_obj;

	int min_filter;
	int mag_filter;
	float anisotropy;

	int compare_func;

	bool repeat_x;
	bool repeat_y;
	bool repeat_z;

	float border_color[4];

	float min_lod;
	float max_lod;
};

struct MGLScope_old {
	PyObject_HEAD

	MGLContext_old * context;
	MGLFramebuffer_old * framebuffer;
	MGLFramebuffer_old * old_framebuffer;

	int * textures;
	int * buffers;

	int num_textures;
	int num_buffers;

	int enable_flags;
	int old_enable_flags;
};

struct MGLTexture_old {
	PyObject_HEAD

	MGLContext_old * context;
	MGLDataType * data_type;

	union {
		int renderbuffer_obj;
		int texture_obj;
	};

	int width;
	int height;
	int components;

	int samples;

	int min_filter;
	int mag_filter;
	int max_level;

	int compare_func;
	int anisotropy;

	bool depth;

	bool repeat_x;
	bool repeat_y;
};

struct MGLTexture3D_old {
	PyObject_HEAD

	MGLContext_old * context;
	MGLDataType * data_type;

	int texture_obj;

	int width;
	int height;
	int depth;

	int components;

	int min_filter;
	int mag_filter;
	int max_level;

	bool repeat_x;
	bool repeat_y;
	bool repeat_z;
};

struct MGLTextureArray_old {
	PyObject_HEAD

	MGLContext_old * context;
	MGLDataType * data_type;

	union {
		int renderbuffer_obj;
		int texture_obj;
	};

	int width;
	int height;
	int layers;
	int components;

	int min_filter;
	int mag_filter;
	int max_level;

	bool repeat_x;
	bool repeat_y;
	float anisotropy;
};

struct MGLTextureCube_old {
	PyObject_HEAD

	MGLContext * context;
	MGLDataType * data_type;

	int texture_obj;

	int width;
	int height;
	int depth;

	int components;

	int min_filter;
	int mag_filter;
	int max_level;
	float anisotropy;
};

struct MGLVertexArray_old {
	PyObject_HEAD

	MGLContext * context;

	MGLProgram_old * program;
	MGLBuffer_old * index_buffer;
	int index_element_size;
	int index_element_type;

	unsigned * subroutines;
	int num_subroutines;

	int vertex_array_obj;
	int num_vertices;
};

extern PyTypeObject * MGLContext_class;
extern PyObject * meth_create_context(PyObject * self, PyObject * const * args, Py_ssize_t nargs);

PyObject * meth_extend_context(PyObject * self, PyObject * args) {
    PyObject * old_context;
    PyObject * glhooks;

    if (!PyArg_ParseTuple(args, "OO", &old_context, &glhooks)) {
        return 0;
    }

    PyObject * newargs[3] = {Py_False, Py_None, glhooks};
    PyObject * new_context = meth_create_context(self, newargs, 3);
    ensure_no_error();
    set_slot(old_context, "new", new_context);
    set_slot(new_context, "old", new_ref(old_context));
    MGLContext_old * old_mglo = (MGLContext_old *)get_slot(old_context, "mglo");
    MGLContext * new_mglo = (MGLContext *)get_slot(new_context, "mglo");
    old_mglo->gl = new_mglo->gl;
    Py_RETURN_NONE;
}

PyObject * meth_extend_buffer(PyObject * self, PyObject * args) {
    PyObject * old_buffer;
    PyObject * new_context;

    if (!PyArg_ParseTuple(args, "OO", &old_buffer, &new_context)) {
        return 0;
    }

	if (!Context_Check(new_context)) {
		return 0;
	}

    MGLBuffer_old * old_mglo = (MGLBuffer_old *)get_slot(old_buffer, "mglo");

	MGLContext * context_mglo = (MGLContext *)get_slot(new_context, "mglo");
    MGLBuffer * buffer = PyObject_New(MGLBuffer, MGLBuffer_class);
    chain_objects(context_mglo, buffer);
    buffer->context = context_mglo;
    buffer->flags = MGL_BUFFER_READABLE | MGL_BUFFER_WRITABLE;
    buffer->buffer_obj = old_mglo->buffer_obj;
    buffer->wrapper = Buffer_New("Nn", buffer, buffer->size);

    set_slot(old_buffer, "new", new_ref(buffer->wrapper));
    set_slot(buffer->wrapper, "old", new_ref(old_buffer));

    Py_RETURN_NONE;
}

PyObject * meth_extend_framebuffer(PyObject * self, PyObject * args) {
    PyObject * old_framebuffer;
    PyObject * new_context;

    if (!PyArg_ParseTuple(args, "OO", &old_framebuffer, &new_context)) {
        return 0;
    }

	if (!Context_Check(new_context)) {
		return 0;
	}

    MGLFramebuffer_old * old_mglo = (MGLFramebuffer_old *)get_slot(old_framebuffer, "mglo");

	MGLContext * context_mglo = (MGLContext *)get_slot(new_context, "mglo");
    MGLFramebuffer * framebuffer = PyObject_New(MGLFramebuffer, MGLFramebuffer_class);

    chain_objects(context_mglo, framebuffer);
    framebuffer->context = context_mglo;
    framebuffer->framebuffer_obj = old_mglo->framebuffer_obj;
    framebuffer->width = old_mglo->width;
    framebuffer->height = old_mglo->height;
    framebuffer->depth = 1;
    // framebuffer->components = old_mglo->components;
    framebuffer->levels = 1;
    framebuffer->samples = old_mglo->samples;
    framebuffer->viewport[0] = old_mglo->viewport_x;
    framebuffer->viewport[1] = old_mglo->viewport_y;
    framebuffer->viewport[2] = old_mglo->viewport_width;
    framebuffer->viewport[3] = old_mglo->viewport_height;
    framebuffer->attachments = old_mglo->draw_buffers_len;
    // char attachment_type[16];
    // unsigned long long color_mask;
    framebuffer->depth_mask = true;
    framebuffer->wrapper = Framebuffer_New("N(ii)", framebuffer, framebuffer->width, framebuffer->height);

    set_slot(old_framebuffer, "new", new_ref(framebuffer->wrapper));
    set_slot(framebuffer->wrapper, "old", new_ref(old_framebuffer));

    Py_RETURN_NONE;
}

PyObject * meth_extend_program(PyObject * self, PyObject * args) {
    PyObject * old_program;
    PyObject * new_context;

    if (!PyArg_ParseTuple(args, "OO", &old_program, &new_context)) {
        return 0;
    }

	if (!Context_Check(new_context)) {
		return 0;
	}

    MGLProgram_old * old_mglo = (MGLProgram_old *)get_slot(old_program, "mglo");

	MGLContext * context_mglo = (MGLContext *)get_slot(new_context, "mglo");
    MGLProgram * program = PyObject_New(MGLProgram, MGLProgram_class);

    chain_objects(context_mglo, program);
    program->context = context_mglo;
    program->program_obj = old_mglo->program_obj;
	PyObject * uniforms = get_uniforms(context_mglo->gl, program->program_obj);
	PyObject * attributes = get_attributes(context_mglo->gl, program->program_obj);
    program->wrapper = Program_New("NNN", program, uniforms, attributes);

    set_slot(old_program, "new", new_ref(program->wrapper));
    set_slot(program->wrapper, "old", new_ref(old_program));

    Py_RETURN_NONE;
}

PyObject * meth_extend_renderbuffer(PyObject * self, PyObject * args) {
    PyObject * old_renderbuffer;
    PyObject * new_context;

    if (!PyArg_ParseTuple(args, "OO", &old_renderbuffer, &new_context)) {
        return 0;
    }

	if (!Context_Check(new_context)) {
		return 0;
	}

    MGLRenderbuffer_old * old_mglo = (MGLRenderbuffer_old *)get_slot(old_renderbuffer, "mglo");
	MGLContext * context_mglo = (MGLContext *)get_slot(new_context, "mglo");
    MGLRenderbuffer * renderbuffer = PyObject_New(MGLRenderbuffer, MGLRenderbuffer_class);

    chain_objects(context_mglo, renderbuffer);
    renderbuffer->context = context_mglo;
    renderbuffer->renderbuffer_obj = old_mglo->renderbuffer_obj;
    renderbuffer->wrapper = Renderbuffer_New("N", renderbuffer);

    set_slot(old_renderbuffer, "new", new_ref(renderbuffer->wrapper));
    set_slot(renderbuffer->wrapper, "old", new_ref(old_renderbuffer));

    Py_RETURN_NONE;
}

PyObject * meth_extend_texture(PyObject * self, PyObject * args) {
    PyObject * old_texture;
    PyObject * new_context;

    if (!PyArg_ParseTuple(args, "OO", &old_texture, &new_context)) {
        return 0;
    }

	if (!Context_Check(new_context)) {
		return 0;
	}

    MGLTexture_old * old_mglo = (MGLTexture_old *)get_slot(old_texture, "mglo");
	MGLContext * context_mglo = (MGLContext *)get_slot(new_context, "mglo");
    MGLTexture * texture = PyObject_New(MGLTexture, MGLTexture_class);

    chain_objects(context_mglo, texture);
    texture->context = context_mglo;
    texture->texture_obj = old_mglo->texture_obj;
    texture->wrapper = Texture_New("Nii(ii)", texture, 0, -1, texture->width, texture->height);

    set_slot(old_texture, "new", new_ref(texture->wrapper));
    set_slot(texture->wrapper, "old", new_ref(old_texture));

    Py_RETURN_NONE;
}

PyObject * meth_extend_refholder(PyObject * self, PyObject * args) {
    PyObject * old_object;
    PyObject * new_context;

    if (!PyArg_ParseTuple(args, "OO", &old_object, &new_context)) {
        return 0;
    }

	MGLContext * context_mglo = (MGLContext *)get_slot(new_context, "mglo");
    MGLRefholder * refholder = PyObject_New(MGLRefholder, MGLRefholder_class);

    chain_objects(context_mglo, refholder);
    refholder->context = context_mglo;
    refholder->wrapper = Refholder_New("N", refholder);

    set_slot(old_object, "new", new_ref(refholder->wrapper));
    set_slot(refholder->wrapper, "old", new_ref(old_object));

    Py_RETURN_NONE;
}

PyObject * get_new_wrapper(PyObject * old_wrapper) {
	if (PyObject_HasAttrString(old_wrapper, "new")) {
    	PyObject * new_wrapper = PyObject_GetAttrString(old_wrapper, "new");
        Py_DECREF(new_wrapper);
        return new_wrapper;
    }
    return old_wrapper;
}
