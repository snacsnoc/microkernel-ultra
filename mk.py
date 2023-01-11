from threading import Semaphore

from filesystem_driver import FileSystemDriver
from device_manager import DeviceManager


class Microkernel:
    MAXIMUM_ALLOWED_MEMORY = 100  # Example maximum allowed memory in bytes

    def __init__(self):
        self.memory = {}
        self.process_list = []
        self.message_queues = {}
        self.file_system_driver = FileSystemDriver()
        self.mount_points = {}
        self.cache = {}
        self.buffer = {}
        self.semaphores = {}
        self.process_queues = {}
        self.lock = Semaphore()
        self.device_manager = DeviceManager()
        self.violation_handlers = {}
        self.memory_allocations = {}

    def lock(self):
        self.lock.acquire()

    def unlock(self):
        self.lock.release()

    def add_process(self, process_id):
        self.lock.acquire()
        self.process_list.append(process_id)
        self.lock.release()
        return True

    def check_process(self, process_id):
        self.lock.acquire()
        check = process_id in self.process_list
        self.lock.release()
        return check

    def stop_process(self, process_id):
        self.lock.acquire()
        self.process_list.remove(process_id)
        self.lock.release()

    def send_message(self, process_id, message):
        """Send a message to a process message queue"""
        if process_id in self.process_queues:
            self.process_queues[process_id].append(message)
            return True
        else:
            return False

    def receive_message(self, process_id):
        """Receive a message from a process message queue"""
        if (
            process_id in self.process_queues
            and len(self.process_queues[process_id]) > 0
        ):
            return self.process_queues[process_id].pop(0)
        else:
            return None

    def read_block(self, device, block_num):
        """Reads a block of data from the specified device"""
        # Check if the block is in the cache
        if (device, block_num) in self.cache:
            return self.cache[(device, block_num)]

        # Check if the block is in the buffer
        if (device, block_num) in self.buffer:
            data = self.buffer.pop((device, block_num))
            self.cache[(device, block_num)] = data
            return data
        print(block_num)
        # Block is not in cache or buffer, read from device
        data = self.device_manager.read_from_device(device, block_num)
        self.cache[(device, block_num)] = data
        return data

    def write_block(self, device, block_num, data):
        """Writes a block of data to the specified device"""
        # If block is in cache, update it
        if (device, block_num) in self.cache:
            self.cache[(device, block_num)] = data

        # If block is in buffer, update it
        elif (device, block_num) in self.buffer:
            self.buffer[(device, block_num)] = data

        # Block is not in cache or buffer, add it to buffer
        else:
            self.buffer[(device, block_num)] = data

    def mount_file_system(self, device, mount_point):
        """Mounts a file system on the specified device at the specified mount point"""
        if mount_point in self.mount_points:
            return False
        else:
            self.mount_points[mount_point] = self.file_system_driver
            return True

    def unmount_file_system(self, mount_point):
        """Unmounts a file system at the specified mount point"""
        if mount_point in self.mount_points:
            del self.mount_points[mount_point]
            return True
        else:
            return False

    def flush_buffer(self):
        """Writes all dirty blocks in the buffer to the device"""
        for (device, block_num), data in self.buffer.items():
            self.write_to_device(device, block_num, data)
        self.buffer.clear()

    def evict_cache(self):
        """Removes the least recently used block from the cache"""
        lru_block = min(self.cache, key=lambda x: self.cache[x][1])
        self.cache.pop(lru_block)

    def create_file(self, path, size):
        """Creates a new file at the specified path with the specified size"""
        if path.startswith("/mnt"):
            mount_point = "/mnt"
        else:
            return None
        if mount_point in self.mount_points:
            return self.mount_points[mount_point].create_file(
                path[len(mount_point) :], size
            )
        else:
            return None

    def delete_file(self, path):
        """Deletes the file at the specified path"""
        if path.startswith("/mnt"):
            mount_point = "/mnt"
        else:
            return None
        if mount_point in self.mount_points:
            return self.mount_points[mount_point].delete_file(path[len(mount_point) :])
        else:
            return None

    def read_file(self, path):
        """Reads the file at the specified path"""
        if path.startswith("/mnt"):
            mount_point = "/mnt"
        else:
            return None
        if mount_point in self.mount_points:
            return self.mount_points[mount_point].read_file(path[len(mount_point) :])
        else:
            return None

    def write_file(self, path, data):
        """Writes data to the file at the specified path"""
        if path.startswith("/mnt"):
            mount_point = "/mnt"
        else:
            return None
        if mount_point in self.mount_points:
            return self.mount_points[mount_point].write_file(
                path[len(mount_point) :], data
            )
        else:
            return None

    def peak_memory(self):
        return self.memory

    def allocate_memory(self, size, process_id):
        """Allocates a block of memory of the specified size for a process"""
        # if not self.check_memory_violation(size, process_id):
        #    return None
        memory_block = {}
        memory_block["id"] = len(self.memory) + 1
        memory_block["size"] = size
        memory_block["allocated"] = True
        memory_block["process_id"] = process_id
        self.memory[memory_block["id"]] = memory_block
        return memory_block

    def check_memory_violation(self, size, process_id):
        """Checks if allocating a block of memory of the specified size for a process would exceed the maximum allowed memory"""
        allocated_memory = sum(
            [
                block["size"]
                for block in self.memory
                if block["process_id"] == process_id and block["allocated"]
            ]
        )
        MAXIMUM_ALLOWED_MEMORY = 100
        if (allocated_memory + size) > MAXIMUM_ALLOWED_MEMORY:
            return False
        else:
            return True

    def free_memory(self, id, process_id):
        """Frees a block of memory with the specified id if the process_id matches"""
        if id in self.memory:
            memory_block = self.memory[id]
            if memory_block["process_id"] == process_id:
                del self.memory[id]
                return True
            else:
                return False
        else:
            return False

    def create_message_queue(self, queue_name):
        """Create a new message queue"""
        self.message_queues[queue_name] = {"lock": Semaphore(), "queue": []}

    def send_message_queue(self, queue_name, message):
        """Send a message to a message queue"""
        if queue_name in self.message_queues:
            self.message_queues[queue_name]["lock"].acquire()
            self.message_queues[queue_name]["queue"].append(message)
            self.message_queues[queue_name]["lock"].release()
            return True
        else:
            return False

    def receive_message_queue(self, queue_name):
        """Receive a message from a message queue"""
        if (
            queue_name in self.message_queues
            and len(self.message_queues[queue_name]["queue"]) > 0
        ):
            self.message_queues[queue_name]["lock"].acquire()
            message = self.message_queues[queue_name]["queue"].pop(0)
            self.message_queues[queue_name]["lock"].release()
            return message
        else:
            return None
