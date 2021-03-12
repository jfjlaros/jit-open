"""Tests for the jit_open library."""
from fake_open import FakeOpen

from jit_open import jit_open, Handle, Queue


class TestLibrary(object):
    def setup(self):
        fake_open = FakeOpen()
        self._handles = fake_open.handles
        self._open = fake_open.open

        self._queue = Queue()

    def test_unused(self):
        handle = Handle('test.txt', self._queue, f_open=self._open)
        assert 'test.txt' not in self._handles

    def test_used_1(self):
        handle = Handle('test.txt', self._queue, f_open=self._open)
        handle.write('line 1\n')
        handle.close()
        assert self._handles['test.txt'].getvalue() == 'line 1\n'

    def test_used_2(self):
        handle = Handle('test.txt', self._queue, f_open=self._open)
        handle.write('line 1\n')
        handle.write('line 2\n')
        handle.close()
        assert self._handles['test.txt'].getvalue() == 'line 1\nline 2\n'
