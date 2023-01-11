from mk import Microkernel

#########
mk = Microkernel()

# create two new processes with IDs 1 and 2

mk.add_process(2)

# allocate memory for process ID 1
mk.allocate_memory(1024, 2)


# send message "Hello from process 1" from process 1 to process 2
mk.send_message(2, "Hello from process 2")

message = mk.receive_message(2)
print(message)


# attempt to receive message from an invalid process ID
message = mk.receive_message(3)
print("attempt to receive message from an invalid process ID", message)
# output: None

# attempting to receive message from process 1 after it has been received
message = mk.receive_message(1)
print(message)


# free memory allocated for process ID 1
mk.free_memory(1, 1)


# Mounting a file system on the device '/dev/sda1' at the mount point '/mnt'
mk.mount_file_system("/dev/sda1", "/mnt")

# create a file named test.txt
mk.create_file("/mnt/test.txt", 10)

# writing to the file
mk.write_file("/mnt/test.txt", b"Hello, world!")

# reading the file
data = mk.read_file("/mnt/test.txt")
print("read from mounted filed: ", data.decode())

# deleting the file
mk.delete_file("/mnt/test.txt")

# unmount the file system
mk.unmount_file_system("/mnt")


# writing to a block on the device '/dev/sda1'
mk.write_block("/dev/sda1", 1, b"This is a block of data")
# read a block from device '/dev/sda1'
data = mk.read_block("/dev/sda1", 1)
print(data)

# flush the buffer
mk.flush_buffer()

# evict a block from the cache
mk.evict_cache()
