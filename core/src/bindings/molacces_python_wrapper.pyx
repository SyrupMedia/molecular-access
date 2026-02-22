cdef extern from "molacces_python.h":
    ctypedef void (*callback_function)(char *name, void *function_on_update_arguments)
    void molecular_ipc_listener_update_callback_python(callback_function function_on_update, void *function_on_update_arguments)

def find(f):
    molecular_ipc_listener_update_callback_python(callback, <void*>f)

cdef void callback(char *name, void *f) noexcept:
    (<object>f)(name.decode('utf-8'))
