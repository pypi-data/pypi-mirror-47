#pragma once
#include "context.hpp"

struct MGLRefholder : public MGLContextObject {
};

extern PyType_Spec MGLRefholder_spec;
extern PyTypeObject * MGLRefholder_class;
