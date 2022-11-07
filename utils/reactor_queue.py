from twisted.internet import reactor


class ReactorQueue:
    def __init__(self, runners_count):
        self.count = runners_count

    def push(self):
        self.count = self.count + 1

    def pop(self):
        self.count = self.count - 1
        if self.count == 0:
            reactor.stop()
