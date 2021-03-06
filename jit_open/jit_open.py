"""Just-in-time open.

This library can be used when a large amount of files need to be opened.

To deal with resource limits, the following techniques are used:
- Data is written to a buffer.
- The file is opened for appending when the buffer is full, the data is then
  written to the file.
- All Handle objects share a Queue. If the total amount of used memory (all
  buffers) exceeds a given maximum, a flushing strategy is executed.

Note that empty files will not be created.
"""
class Queue(object):
    """Queue for Handle objects."""
    def __init__(self, max_size=1073741824):
        """
        :arg int max_size: Maximum size of the memory buffer.
        """
        self.max_size = max_size
        self.size = 0

        self._queue = []

    def append(self, item):
        self._queue.append(item)

    def flush(self):
        for item in self._queue:
            item.flush()


class Handle(object):
    """Set up a just-in-time file open handle like object."""
    def __init__(self, name, queue, max_size=1048576, f_open=open, mode='t'):
        """
        :arg str name: Name of the file.
        :arg Queue queue: Queue for open files.
        :arg int max_size: Maximum size of the memory buffer.
        :arg function opener: File open function.
        :arg str mode: File mode ('t' for text, 'b' for binary).
        """
        self.name = name
        self._queue = queue
        self._max_size = max_size
        self._open = f_open
        self._mode = mode

        self._buffer = ''
        self._queue.append(self)

    def __exit__(self):
        self.flush()

    def flush(self):
        if self._buffer:
            handle = self._open(self.name, 'a' + self._mode)
            handle.write(self._buffer)
            handle.close()

            self._queue.size -= len(self._buffer)
            self._buffer = ''

    def close(self):
        self.flush()

    def write(self, data):
        if len(self._buffer) > self._max_size:
            if self._queue.size > self._queue.max_size:
                self._queue.flush()
            else:
                self.flush()

        self._buffer += data
        self._queue.size += len(data)
