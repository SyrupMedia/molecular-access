#pragma once

#include <iostream>
#include <functional>
#include <thread>
#include <memory>

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
    LOW    = 0,
    MEDIUM = 1,
    HIGH   = 2,
    ACTUAL = 3, // Highest priority, should be reserved for immediate transfer.
};

enum molecular_ipc_route_type {
    PRODUCER = 0,
    CONSUMER = 1
};

struct molecular_ipc {
    std::shared_ptr<ipc::route> molecular_ipc_route;
    const char *molecular_ipc_route_name;
    molecular_ipc_route_type molecular_ipc_route_type_value;
};