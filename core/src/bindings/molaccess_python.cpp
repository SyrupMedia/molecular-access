#include <iostream>
#include <functional>

#include "molaccess.hpp"
#include "molaccess_python.hpp"

ManagedProducer::ManagedProducer(const char *name) {
    ipc_instance = molecular_ipc_producer_create(name);
}

void ManagedProducer::send_data(const char *data) {

    ipc_instance.molecular_ipc_route->wait_for_recv(1);

    molecular_send(ipc_instance, data);

    ipc_instance.molecular_ipc_route->send(ipc::buff_t('\0'));

}

ManagedConsumer::ManagedConsumer(const char *name) {
    ipc_instance = molecular_ipc_listener_create(name);
}

void listener_update(
    molecular_ipc &molecular_ipc_target, 
    std::function<void(const char*)> callback
) {

    while (1) {
        auto buf = molecular_ipc_target.molecular_ipc_route->recv();
        auto str = static_cast<char *>(buf.data());

        if (str == nullptr || str[0] == '\0') {
            return;
        }

        callback(str);
    }
}

void ManagedConsumer::subscribe_update(PyObject *callback) {

    std::function<void(const char*)> update = [callback](const char *data) {
        PyObject *data_py = Py_BuildValue("(s)", data);
        PyObject_CallObject(callback, data_py);
    };

    listener_update(ipc_instance, update);

}
