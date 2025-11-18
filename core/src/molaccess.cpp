#include "molaccess.hpp"
#include "molaccess_ipc.hpp"

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