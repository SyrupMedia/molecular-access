def listener_update(_callback: callable):
    pass
    # while True:
    # Run callback whenever data is received from the TCP channel


class ManagedProducer:
    def __init__(self, name):
        # To do: Create TCP connection
        ipc_instance = None

    def send_data(self, data_string):
        print(f"Sending data {data_string} (not really)")


class ManagedConsumer:
    def __init__(self, name):
        # To do: Create TCP connection
        ipc_instance = None

    def subscribe_update(self, callback: callable):
        listener_update(callback)
