from filesystem import FileSystem


class FileSystemDriver:
    def __init__(self):
        self.file_system = FileSystem()

    def create_file(self, name, size):
        """Creates a new file with the specified name and size"""
        return self.file_system.create_file(name, size)

    def delete_file(self, name):
        """Deletes the specified file"""
        return self.file_system.delete_file(name)

    def read_file(self, name):
        """Reads the specified file"""
        return self.file_system.read_file(name)

    def write_file(self, name, data):
        """Writes data to the specified file"""
        return self.file_system.write_file(name, data)
