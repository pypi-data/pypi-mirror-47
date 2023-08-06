#include "refholder.hpp"
#include "context.hpp"

void MGLRefholder_dealloc(MGLRefholder * self) {
    Py_TYPE(self)->tp_free(self);
}

PyType_Slot MGLRefholder_slots[] = {
    {Py_tp_dealloc, (void *)MGLRefholder_dealloc},
    {0},
};

PyType_Spec MGLRefholder_spec = {
    "moderngl.mgl.new.MGLRefholder",
    sizeof(MGLRefholder),
    0,
    Py_TPFLAGS_DEFAULT,
    MGLRefholder_slots,
};

PyTypeObject * MGLRefholder_class;
