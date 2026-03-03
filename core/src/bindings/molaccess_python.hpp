#include <Python.h>

#include "molaccess_ipc.hpp"

// TODO: Make abstract
class MolecularManaged {
protected:
    molecular_ipc ipc_instance;
};

class ManagedProducer: public MolecularManaged {
public:
    ManagedProducer(const char *i_name);
    void send_data(const char *data);
};

class ManagedConsumer: public MolecularManaged {
public:
    ManagedConsumer(const char *i_name);
    void subscribe_update(PyObject *callback);
};
