#pragma once

#include <iostream>
#include <functional>
#include <thread>
#include <memory>

#include <libipc/ipc.h>

#include "molaccess_ipc.hpp"

typedef struct molecular_message {
    const char *message_data;
    molecular_message_type message_type;
} molecular_message;

void molecular_say_hello();

void molecular_send(molecular_ipc &molecular_ipc_target, const char *message_data);

molecular_ipc molecular_ipc_producer_create(const char *molecular_ipc_route_name_init);

molecular_ipc molecular_ipc_listener_create(const char *molecular_ipc_route_name_init);
void molecular_ipc_listener_update(
        molecular_ipc &molecular_ipc_target, 
        void(*function_on_update)(char*));