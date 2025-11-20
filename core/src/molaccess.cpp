#include "molaccess.hpp"
#include "molaccess_ipc.hpp"

void molecular_say_hello() {
    std::cout << "Hello, from Molecular!" << '\n';
}

void molecular_send(molecular_ipc &molecular_ipc_target, const char *message_data) {
    molecular_ipc_target.molecular_ipc_route->send(message_data);
}

molecular_ipc molecular_ipc_producer_create(const char *molecular_ipc_route_name_init) {
    molecular_ipc molecular_ipc_init = {
        std::shared_ptr<ipc::route> {new ipc::route { molecular_ipc_route_name_init }},
        molecular_ipc_route_name_init,
        PRODUCER
    };

    return molecular_ipc_init;
}

molecular_ipc molecular_ipc_listener_create(const char *molecular_ipc_route_name_init) {
    molecular_ipc molecular_ipc_init = {
        std::shared_ptr<ipc::route> {new ipc::route { molecular_ipc_route_name_init, ipc::receiver }},
        molecular_ipc_route_name_init,
        CONSUMER
    };

    return molecular_ipc_init;
}

void molecular_ipc_listener_update(
        molecular_ipc &molecular_ipc_target, 
        void(*function_on_update)(char*)
    ) {
    std::printf("Running update cycle.\n");

    while (1) {
        auto buf = molecular_ipc_target.molecular_ipc_route->recv();
        auto str = static_cast<char *>(buf.data());

        if (str == nullptr || str[0] == '\0') {
            return;
        }

        (*function_on_update)(str);
    }
}