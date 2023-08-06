==========
Random I/O
==========

Generate test files object easily. For instance create 16 bytes file: ::

    >>> import randomio
    >>> gen = randomio.FileGenerator(size=16)
    >>> gen.read()
    '\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
