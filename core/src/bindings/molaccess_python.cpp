#include <iostream>

#include "molaccess.hpp"
#include "molaccess_python.hpp"

void molecular_ipc_listener_update_callback_python(
    PyObject *function_on_update,
    PyObject *function_on_update_arguments
) {
    std::cout << "Calling Python callback function" << '\n';

    PyObject_CallObject(function_on_update, function_on_update_arguments);
}