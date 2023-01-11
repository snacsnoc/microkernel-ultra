class Sem:
    def __init__(self):
        self.semaphores = {}

    def sem_acquire(self, name):
        if name in self.semaphores:
            semaphore = self.semaphores[name]
            if semaphore["count"] > 0:
                semaphore["count"] -= 1
                return True
            else:
                return False
        else:
            return False

    def sem_release(self, name):
        if name in self.semaphores:
            semaphore = self.semaphores[name]
            semaphore["count"] += 1
            return True
        else:
            return False

    def sem_create(self, name, initial_count):
        if name in self.semaphores:
            return False
        else:
            semaphore = {"count": initial_count}
            self.semaphores[name] = semaphore
            return True
