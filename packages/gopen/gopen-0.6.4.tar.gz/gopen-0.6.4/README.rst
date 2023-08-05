=====
gopen
=====
Provides the **gopen.readable()** and **gopen.gread()** functions.

**readable(source)** supports `with` statements for readable file objects::

  >>> with gopen.readable(source) as f:
  >>>     <read from f>

**gread(source)** returns an iterator over input lines::

  >>> from gopen import gread
  >>> lines = gread(source)
  >>> lines
  <generator object gread at 0x7f45752ebf10>

**<source>** can be:

* a readable file object,
* a file descriptor and
* a file pathname.

gzip and bzip2-compressed files will be decompressed on the fly.
No side effects: if `source` is a file descriptor or a file handle,
it will not be closed.

Example::

  >>> f = open('txt', 'r')
  >>> for source in ['txt', 'txt.gz', 'txt.bz2', f]:
  ...     print('%r (%r)' % (list(gread(source)), source))
  ...
  ['Simple is\n', 'better than complex.'] ('txt')
  ['Simple is\n', 'better than complex.'] ('txt.gz')
  ['Simple is\n', 'better than complex.'] ('txt.bz2')
  ['Simple is\n', 'better than complex.'] (<_io.TextIOWrapper name='txt' mode='r' encoding='UTF-8'>)
  >>> f.closed
  False

Changes
=======
0.6 (2019-05-27)
----------------
- Python3 only (>= 3.4)
