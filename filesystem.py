class FileSystem:
    def __init__(self):
        self.files = {}
        self.free_space = 1024  # Total size of the file system in bytes

    def create_file(self, name, size):
        """Creates a new file with the specified name and size"""
        if self.free_space >= size:
            file = {"name": name, "size": size, "data": ""}
            self.files[name] = file
            self.free_space -= size
            return file
        else:
            return None

    def delete_file(self, name):
        """Deletes the specified file"""
        if name in self.files:
            file = self.files[name]
            del self.files[name]
            self.free_space += file["size"]
            return True
        else:
            return False

    def read_file(self, name):
        """Reads the specified file"""
        if name in self.files:
            return self.files[name]["data"]
        else:
            return None

    def write_file(self, name, data):
        """Writes data to the specified file"""
        if name in self.files:
            self.files[name]["data"] = data
            return True
        else:
            return False
