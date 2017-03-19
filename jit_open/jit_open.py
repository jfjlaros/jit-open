import heapq
import resource


class Queue(list):
    def __init__(self, max_size=0, *args, **kwargs):
        self.max_size = max_size

        super(Queue, self).__init__(*args, **kwargs)
        if not self.max_size:
            self.max_size = resource.getrlimit(resource.RLIMIT_NOFILE)[0] - 100


class Handle(object):
    def __init__(self, name, queue):
        self._name = name
        self._queue = queue

        self._count = 0
        self._handle = None
        self.write = self._append

    def __lt__(self, y):
        return self._count < y._count

    def _write(self, *args, **kwargs):
        self._handle.write(*args, **kwargs)
        self._count += 1

    def _append(self, *args, **kwargs):
        if len(self._queue) > self._queue.max_size:
            heapq.heapify(self._queue) # Not as efficient as could be.
            heapq.heappop(self._queue).suspend()
        heapq.heappush(self._queue, self)

        self._handle = open(self._name, 'a+')
        self.write = self._write
        self.write(*args, **kwargs)

    def suspend(self):
        self._handle.close()
        self.write = self._append
