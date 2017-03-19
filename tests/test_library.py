"""
Tests for the jit_open library.
"""
from __future__ import unicode_literals

from fake_open import FakeOpen

from jit_open import jit_open, Handle, Queue


class TestLibrary(object):
    def setup(self):
        opener = FakeOpen()
        self._handles = opener.handles
        jit_open.open = opener.open

        self._queue = Queue()

    def test_unused(self):
        handle = Handle('test.txt', self._queue)
        assert 'test.txt' not in self._handles

    def test_used_1(self):
        handle = Handle('test.txt', self._queue)
        handle.write('line 1\n')
        assert self._handles['test.txt'].getvalue() == 'line 1\n'

    def test_used_2(self):
        handle = Handle('test.txt', self._queue)
        handle.write('line 1\n')
        handle.write('line 2\n')
        assert self._handles['test.txt'].getvalue() == 'line 1\nline 2\n'
