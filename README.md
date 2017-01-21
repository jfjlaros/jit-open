# Just in time open files.
This package provides a way to delay opening files until the something is
written to the file handle. This can be convenient when opening a large number
of files of which most of them will not be used.

## Installation
Via [pypi](https://pypi.python.org/pypi/jit-open):

    pip install jit_open

From source:

    git clone https://git.lumc.nl/j.f.j.laros/jit-open.git
    cd jit_open
    pip install .

## Library
The library provides the `JITOpen` class. Full documentation can be found
[here](https://git.lumc.nl/j.f.j.laros/jit-open).

### Usage
In the following example, only the file `used.txt` is created.

```python
>>> from jit_open import JITOpen
>>>
>>> used = JITOpen("used.txt", "w")
>>> unused = JITOpen("unused.txt", "w")
>>>
>>> used.write("line 1\n")
>>> used.write("line 2\n")
```
