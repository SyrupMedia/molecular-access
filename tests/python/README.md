# Tests
## Bindings
The [`bindings`](bindings/src) test is composed of two Python scripts, using 
the Molecular Access API bindings, generated using Swig. It demonstrates a 
simple client-server setup where one IPC instance, the client, receives a 
string from another IPC instance, the server. Subsequently, the client calls a
callback function using the string as an input. 

> [!IMPORANT] 
> It is important to note that the Molecular Access API does not internally
> recognise 'server' or 'client' processes. Everything is treated as an IPC
> instance, and any instance can choose to freely receive or transmit data.

### Running
This test requires both the `client.py` and `server.py` scripts to run. This 
can be done by running each script in seperate terminal sessions, or
alternatively by running the `run.sh` script. This is the recommended way.

```sh
➜ cd bindings/src
➜ sh run.sh
```

#### Manually
1. Run this in one terminal:

```sh
➜ python3 client.py
```

2. Run this in another terminal:

```sh
➜ python3 server.py
```
