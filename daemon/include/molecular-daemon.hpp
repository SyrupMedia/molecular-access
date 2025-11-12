#pragma once

#include <iostream>
#include <functional>
#include <thread>

#include <libipc/ipc.h>

enum molecular_message_type {
    CLOSE,
    READ,
    CREATE,
    UPDATE,
    SET,
    RESET,
    LOCK,
    UNLOCK,
    STAT,
};

enum molecular_message_priority {
    LOW = 0,
    MEDIUM = 1,
    HIGH = 2,
    ACTUAL = 3, // Highest priority, should be reserved for immediate transfer.
};

enum molecular_ipc_route_type {
    PRODUCER = 0,
    CONSUMER = 1
};

typedef struct molecular_ipc {
    ipc::route molecular_ipc_route;
    const char* molecular_ipc_route_name;
    molecular_ipc_route_type molecular_ipc_route_type_value;
} molecular_ipc;

typedef struct molecular_message {
    const char* message_data;
    molecular_message_type message_type;
} molecular_message;

void molecular_send(molecular_ipc &molecular_ipc_target, const char* message_data);
molecular_ipc molecular_ipc_producer_create(const char* molecular_ipc_route_name_init);
molecular_ipc molecular_ipc_listener_create(const char* molecular_ipc_route_name_init);