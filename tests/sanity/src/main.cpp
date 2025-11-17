#include <iostream>
#include <thread>

#include <libipc/ipc.h>

std::vector<char const *> const data_vector_test = {
    "Hello,",
    "world!",
};

int main() {
    std::thread thread_producer {[&] {
        ipc::route ipc_route { "molecular-test-route" };

        ipc_route.wait_for_recv(1);
    
        for (auto str : data_vector_test) {
            ipc_route.send(str);
        }
   
        ipc_route.send(ipc::buff_t('\0'));
    }};
    
    std::thread thread_consumer {[&] {
        ipc::route ipc_route { "molecular-test-route", ipc::receiver };
        
        while (1) {
            auto buf = ipc_route.recv();
            auto str = static_cast<char*>(buf.data());

            if (str == nullptr || str[0] == '\0') {
                return 0;
            }

            std::printf("Received: %s\n", str);
        }
    }};

    thread_producer.join();
    thread_consumer.join();
    
    return 0;
}