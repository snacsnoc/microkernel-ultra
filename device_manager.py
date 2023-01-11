class DeviceManager:
    def __init__(self):
        self.devices = {}

    def register_device(self, device_name, block_size):
        """Register a device with the given name and block size"""
        self.devices[device_name] = block_size

    def read_from_device(self, device_name, block_number):
        """Read a block from a registered device"""
        if device_name in self.devices:
            block_size = self.devices[device_name]
            with open(device_name, "rb") as f:
                f.seek(block_number * block_size)
                return f.read(block_size)
        else:
            raise ValueError(f"{device_name} is not a registered device")
