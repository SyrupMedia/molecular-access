#include <iostream>
#include <thread>

#include <libipc/ipc.h>

#include "molaccess.hpp"

std::vector<char const *> const data_vector_test = {
    "Hello",
    "world!",
};

void molecular_ipc_listener_update_callback(char* input_string) {
    std::cout << input_string << "!!!" << '\n';
}

int main(void) {
    std::thread thread_producer { [&] {
                                      std::cout << "Running daemon.\nInitialising libipc IPC route!\n";

                                      molecular_ipc molecular_ipc_instance = molecular_ipc_producer_create("molaccesd-ipc-route");

                                      molecular_ipc_instance.molecular_ipc_route->wait_for_recv(1);

                                      for (auto str : data_vector_test) {
                                          molecular_send(molecular_ipc_instance, str);
                                      }

                                      molecular_ipc_instance.molecular_ipc_route->send(ipc::buff_t('\0'));
                                  } };

    std::thread thread_consumer { [&] {
                                      std::cout << "Running client.\nInitialising libipc IPC route!\n";

                                      molecular_ipc molecular_ipc_instance = molecular_ipc_listener_create("molaccesd-ipc-route");

                                      molecular_ipc_listener_update(molecular_ipc_instance, molecular_ipc_listener_update_callback);
                                  } };

    thread_producer.join();
    thread_consumer.join();

    return 0;
}