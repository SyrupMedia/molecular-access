# Protocol Specification
## Messages
A message is a call to a method, formatted as a JSON string. Messages must
contain the desired method to be called, along with arguments required by the
method. Most methods require a target resource ID to be passed as an argument.

In practice, methods are comparable to HTTP request methods.

### Methods
The full list of methods consists of:
- `CLOSE`
- `READ`
- `CREATE`
- `UPDATE`
- `SET`
- `RESET`
- `LOCK`
- `UNLOCK`
- `STAT`
- `CALL`

-------------------------------------------------------------------------------

#### `CLOSE`
This method will notify the receiving connection to close its route, and end
all traffic with the sender.

This method takes no arguments.

-------------------------------------------------------------------------------

#### `READ`
Requests the value of a resource.

#### Required Arguments
- `resource_id`
    - The index of the target resource.

-------------------------------------------------------------------------------

#### `CREATE`
Creates a new resource in the collection associated with the connection route.

#### Required Arguments
- `resource_id`
    - The index of the target resource.
- `value_default`
    - The default value of the resource upon creation.
    - Future changes of the value can be undone with the `RESET` method.

-------------------------------------------------------------------------------

#### `UPDATE`
Submits the value of a resource. Causes side-effects which may mutate 
additional resources or data.

#### Required Arguments
- `resource_id`
    - The index of the target resource.
- `value_new`
    - The new value of the resource.

-------------------------------------------------------------------------------

#### `SET`
Submits the value of a resource, without causing any side-effects. `SET` is
idempotent, whereas a `UPDATE` call might result in different data depending on
the result.

#### Required Arguments
- `resource_id`
    - The index of the target resource.
- `value_new`
    - The new value of the resource.

-------------------------------------------------------------------------------

#### `RESET`
Reset the value of a resource to its default value, as determined through the
daemon.

#### Required Arguments
- `resource_id`
    - The index of the target resource.

-------------------------------------------------------------------------------

#### `LOCK`
Lock a resource, prevent its value from being modified.

#### Required Arguments
- `resource_id`
    - The index of the target resource.

-------------------------------------------------------------------------------

#### `UNLOCK`
Unlocks a resource, allows its value to be modified.

#### Required Arguments
- `resource_id`
    - The index of the target resource.

-------------------------------------------------------------------------------

#### `STAT`
Requests all metadata associated with a resource. Metadata associated with a
a resource includes:
- The resource's data type.
- Methods which may be called on the resource.
- The resource's lock state.
- The resource's default value, if specified.
- The timestamp of the resource's creation.
- The timestamp of the resource's last modification.
- External methods the resource contains which may be called through `CALL`

#### Required Arguments
- `resource_id`
    - The index of the target resource.

-------------------------------------------------------------------------------

#### `CALL`
Requests the execution of an RPC method, defined through the server daemon. 
Such methods are callbacks in programs that can be defined through the 
Molecular API. These methods are stored inside of resources.

#### Required Arguments
- `resource_id`
    - The index of the target resource.
- `method` 
    - The name of the method to be called.

-------------------------------------------------------------------------------

#### Message Priority

Each method call must be associated with a priority index, such as:
- `LOW`
- `MEDIUM`
- `HIGH`
- `ACTUAL`
