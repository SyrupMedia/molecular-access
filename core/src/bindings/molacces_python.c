#include "molacces_python.h"

void molecular_ipc_listener_update_callback_python(callback_function function_on_update, void *function_on_update_arguments) {
  function_on_update("Nyaaa!!! Hello, from C!!!!!!", function_on_update_arguments);
}

