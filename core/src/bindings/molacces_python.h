typedef void (*callback_function)(char *name, void *function_on_update_arguments);
void molecular_ipc_listener_update_callback_python(callback_function function_on_update, void *function_on_update_arguments);
