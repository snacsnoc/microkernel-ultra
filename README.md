# microkernel-ultra 
This is a simple implementation of a microkernel, it simulates the basic functionalities of a microkernel, it can manage processes, memory, message queues, and file systems, as well as a cache and buffer for a virtual file system.

## Features
1. Process management:
* The microkernel can add and check for processes by their process IDs.
2. Memory management:
* The microkernel can allocate and free blocks of memory for processes based on their process IDs.
* The microkernel has a function called `check_memory_violation` that it can use to check if a process is using more memory than it is allowed.
3. Message queues:
* Send and receive messages to and from process message queues.
4. File systems:
* Mount and unmount file systems on specified devices at specified mount points
* It can create, read, write and delete files
* The microkernel has a cache and buffer for virtual filesystem, it uses to store data
5. Semaphores:
* The microkernel has implemented semaphores itself and can acquire and release semaphores for synchronizing access to shared resources (testing)
6. Device management:
* microkernel-ultra can read and write blocks from/to [a virtual] device
* It also has a function to flush dirty blocks from buffer and to evict blocks from cache.
## Usage

```python
from mk import Microkernel

# create a new Microkernel instance
mk = Microkernel()

# create a new process with ID 1
mk.add_process(1)

# allocate 1024 bytes of memory for process ID 1
memory_block = mk.allocate_memory(1024, 1)

# send message "Hello from process 1" from process 1 to process 2
mk.send_message(2, "Hello from process 1")

# receive message from process 2
message = mk.receive_message(2)
print(message)  # "Hello from process 1"

# free memory allocated for process ID 1
mk.free_memory(memory_block["id"], 1)

# mount a file system on the device '/dev/sda1' at the mount point '/mnt'
mk.mount_file_system("/dev/sda1", "/mnt")

# create a file named test.txt
mk.create_file("/mnt/test.txt", 10)

# write data to the file
mk.write_file("/mnt/test.txt", b"Hello, world!")

# read data from the file
data = mk.read_file("/mnt/test.txt")
print("Data read from file:", data.decode())

# delete the file
mk.delete_file("/mnt/test.txt")

# unmount the file system
mk.unmount_file_system("/mnt")

# write data to a block on the device '/dev/sda1'
mk.write_block("/dev/sda1", 1, b"This is a block of data")

# read a block from device '/dev/sda1'
data = mk.read_block("/dev/sda1", 1)
print(data)

# flush the buffer
mk.flush_buffer()

# evict a block from the cache
mk.evict_cache()

```
# IPC
microkernel-ultra offers two different ways for inter-process communication (IPC) using message queues: `send_message()` and `send_message_queue()`.

`send_message()` allows for sending a message directly to a specific process's message queue, specified by the process ID. If the specified process ID is not found in the list of registered processes, the message is not sent and the method returns False.

On the other hand, `create_message_queue()` creates a new message queue and `send_message_queue()` allows for sending a message to a specific message queue, specified by the queue name. 
The message is appended to the queue and it can be received by any process that has access to the queue.

Additionally, using `send_message_queue()` instead of `send_message()` allows you to easily implement pub-sub or fan-out patterns, where multiple processes can receive the same message from the same queue.

`create_message_queue()` can be used to create a new message queue with a specific name, while `send_message_queue()` allows to sending a message to a specific queue.
`send_message_queue()` will fail when the `queue_name` is not exist in the `message_queues` and it will return False. This can be useful in situations where multiple processes need to communicate with each other using a shared message queue, and the specific process that the message is intended for is not known.

To create a new message queue, use the `create_message_queue` method, passing in a name for the queue.


`mk.create_message_queue("queue1")`
To send a message to a message queue, use the send_message_queue method, passing in the name of the queue and the message you want to send.


`mk.send_message_queue("queue1", "Hello from process 1")`
To receive a message from a message queue, use the receive_message_queue method, passing in the name of the queue.

```python
message = mk.receive_message_queue("queue1")
print(message)
```
Please note that the message queue uses Semaphore for thread-safety, message queues will be thread safe when accessed from different processes.