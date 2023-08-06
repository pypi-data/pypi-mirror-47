#include "glsl.hpp"
#include "opengl/opengl.hpp"

/* Remove the rightmost leading brackets.
 */
void clean_glsl_name2(char * name, int & name_len) {
    if (name_len && name[name_len - 1] == ']') {
        name_len -= 1;
        while (name_len && name[name_len] != '[') {
            name_len -= 1;
        }
    }
    name[name_len] = 0;
}

int swizzle_from_chr(char c) {
	switch (c) {
		case 'R':
		case 'r':
			return GL_RED;

		case 'G':
		case 'g':
			return GL_GREEN;

		case 'B':
		case 'b':
			return GL_BLUE;

		case 'A':
		case 'a':
			return GL_ALPHA;

		case '0':
			return GL_ZERO;

		case '1':
			return GL_ONE;
	}

	return -1;
}

char chr_from_swizzle(int c) {
	switch (c) {
		case GL_RED:
			return 'R';

		case GL_GREEN:
			return 'G';

		case GL_BLUE:
			return 'B';

		case GL_ALPHA:
			return 'A';

		case GL_ZERO:
			return '0';

		case GL_ONE:
			return '1';
	}

	return '?';
}

/* GLSL type info.
 */
GLTypeInfo type_info(int type) {
    GLTypeInfo info = {};

    int & cols = info.cols;
    int & rows = info.rows;
    int & shape = info.shape;

    switch (type) {
        case GL_FLOAT: cols = 1; rows = 1; shape = 'f'; break;
        case GL_FLOAT_VEC2: cols = 2; rows = 1; shape = 'f'; break;
        case GL_FLOAT_VEC3: cols = 3; rows = 1; shape = 'f'; break;
        case GL_FLOAT_VEC4: cols = 4; rows = 1; shape = 'f'; break;
        case GL_DOUBLE: cols = 1; rows = 1; shape = 'd'; break;
        case GL_DOUBLE_VEC2: cols = 2; rows = 1; shape = 'd'; break;
        case GL_DOUBLE_VEC3: cols = 3; rows = 1; shape = 'd'; break;
        case GL_DOUBLE_VEC4: cols = 4; rows = 1; shape = 'd'; break;
        case GL_INT: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_VEC2: cols = 2; rows = 1; shape = 'i'; break;
        case GL_INT_VEC3: cols = 3; rows = 1; shape = 'i'; break;
        case GL_INT_VEC4: cols = 4; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT: cols = 1; rows = 1; shape = 'u'; break;
        case GL_UNSIGNED_INT_VEC2: cols = 2; rows = 1; shape = 'u'; break;
        case GL_UNSIGNED_INT_VEC3: cols = 3; rows = 1; shape = 'u'; break;
        case GL_UNSIGNED_INT_VEC4: cols = 4; rows = 1; shape = 'u'; break;
        case GL_BOOL: cols = 1; rows = 1; shape = 'p'; break;
        case GL_BOOL_VEC2: cols = 2; rows = 1; shape = 'p'; break;
        case GL_BOOL_VEC3: cols = 3; rows = 1; shape = 'p'; break;
        case GL_BOOL_VEC4: cols = 4; rows = 1; shape = 'p'; break;
        case GL_FLOAT_MAT2: cols = 2; rows = 2; shape = 'f'; break;
        case GL_FLOAT_MAT3: cols = 3; rows = 3; shape = 'f'; break;
        case GL_FLOAT_MAT4: cols = 4; rows = 4; shape = 'f'; break;
        case GL_FLOAT_MAT2x3: cols = 3; rows = 2; shape = 'f'; break;
        case GL_FLOAT_MAT2x4: cols = 4; rows = 2; shape = 'f'; break;
        case GL_FLOAT_MAT3x2: cols = 2; rows = 3; shape = 'f'; break;
        case GL_FLOAT_MAT3x4: cols = 4; rows = 3; shape = 'f'; break;
        case GL_FLOAT_MAT4x2: cols = 2; rows = 4; shape = 'f'; break;
        case GL_FLOAT_MAT4x3: cols = 3; rows = 4; shape = 'f'; break;
        case GL_DOUBLE_MAT2: cols = 2; rows = 2; shape = 'd'; break;
        case GL_DOUBLE_MAT3: cols = 3; rows = 3; shape = 'd'; break;
        case GL_DOUBLE_MAT4: cols = 4; rows = 4; shape = 'd'; break;
        case GL_DOUBLE_MAT2x3: cols = 3; rows = 2; shape = 'd'; break;
        case GL_DOUBLE_MAT2x4: cols = 4; rows = 2; shape = 'd'; break;
        case GL_DOUBLE_MAT3x2: cols = 2; rows = 3; shape = 'd'; break;
        case GL_DOUBLE_MAT3x4: cols = 4; rows = 3; shape = 'd'; break;
        case GL_DOUBLE_MAT4x2: cols = 2; rows = 4; shape = 'd'; break;
        case GL_DOUBLE_MAT4x3: cols = 3; rows = 4; shape = 'd'; break;
        case GL_SAMPLER_1D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_2D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_3D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_CUBE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_1D_SHADOW: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_2D_SHADOW: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_1D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_2D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_1D_ARRAY_SHADOW: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_2D_ARRAY_SHADOW: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_2D_MULTISAMPLE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_2D_MULTISAMPLE_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_CUBE_SHADOW: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_BUFFER: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_2D_RECT: cols = 1; rows = 1; shape = 'i'; break;
        case GL_SAMPLER_2D_RECT_SHADOW: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_1D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_2D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_3D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_CUBE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_1D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_2D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_2D_MULTISAMPLE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_2D_MULTISAMPLE_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_BUFFER: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_SAMPLER_2D_RECT: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_1D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_2D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_3D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_CUBE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_1D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_2D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_2D_MULTISAMPLE_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_BUFFER: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_SAMPLER_2D_RECT: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_1D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_2D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_3D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_2D_RECT: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_CUBE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_BUFFER: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_1D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_2D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_2D_MULTISAMPLE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_IMAGE_2D_MULTISAMPLE_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_1D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_2D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_3D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_2D_RECT: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_CUBE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_BUFFER: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_1D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_2D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_2D_MULTISAMPLE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_INT_IMAGE_2D_MULTISAMPLE_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_1D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_2D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_3D: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_2D_RECT: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_CUBE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_BUFFER: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_1D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_2D_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_IMAGE_2D_MULTISAMPLE_ARRAY: cols = 1; rows = 1; shape = 'i'; break;
        case GL_UNSIGNED_INT_ATOMIC_COUNTER: cols = 1; rows = 1; shape = 'i'; break;
    }

    return info;
}
