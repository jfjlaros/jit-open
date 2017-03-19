"""Just-in-time open.

This library can be used when a large amount of files need to be opened, of
which a small amount is written to regularly.

To deal with resource limits, and to keep the most frequently used files open,
the following techniques are used:
- Instead of opening a file immediately, open it on the first write.
- Keep the open files in a queue, if the queue is full, close the least used
  file.

Note that empty files will not be created.
"""
import heapq
import resource


class Queue(list):
    def __init__(self, max_size=0, *args, **kwargs):
        """Make list with an additional `max_size` attribute.
        
        If no size is given, use a value based on the soft NOFILE resource
        limit.
        """
        self.max_size = max_size

        super(Queue, self).__init__(*args, **kwargs)
        if not self.max_size:
            self.max_size = resource.getrlimit(resource.RLIMIT_NOFILE)[0] - 100


class Handle(object):
    def __init__(self, name, queue):
        """Set up a just-in-time file open handle like object.

        :arg str name: Name of the file.
        :arg Queue queue: Queue for open files.
        """
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
        """Open a file for appending.

        If too many files are open, first close the one that is least used.
        """
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
