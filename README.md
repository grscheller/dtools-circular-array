# Python Circular Array Implementation

Best used as either a standalone improved Python list or in the
implementing of other Python data structures.

* Python module implementing an indexable, double sided queue
* See [grscheller.circular-array][1] project on PyPI
* See [Detailed API documentation][2] on GH-Pages
* See [Source code][3] on GitHub

## Overview

The CircularArray class implements an auto-resizing, indexable, double
sided queue data structure. O(1) indexing and O(1) pushes and pops
either end. Useful if used directly as an improved version of a Python
List and in the implementation of other data structures in a "has-a"
relationship.

## Usage

```python
from grscheller.circular_array.ca import CA

ca = CA(1, 2, 3)
assert ca.popF_unsafe() == 1
assert ca.popR_unsafe() == 3
ca.pushR(42, 0)
assert repr(ca) == 'CA(2, 42, 0)'
assert str(ca) == '(|2, 42, 0|)'

ca = CA(*range(1,11))
assert repr(ca) == 'CA(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)'
assert str(ca) == '(|1, 2, 3, 4, 5, 6, 7, 8, 9, 10|)'
assert len(ca) == 10
tup3 = ca.popF(3)
tup4 = ca.popR(4)
assert tup3 == (1, 2, 3)
assert tup4 == (10, 9, 8, 7)

assert ca == CA(4, 5, 6)
out = ca.popF(1000)
assert out == (4, 5, 6)

assert ca == CA(1, 2)
out, = ca.popF(1, 42)
assert out == 1
out, = ca.popF(default=42)
assert out == 2
out, = ca.popF(default=42)
assert out == 42

assert (42,) == CA().popF(default=42) == CA().popF(num=1, default=42)
assert (42,) == CA().popF(1, default=42)  # 1 is special
assert () == CA().popF(2, default=42)
assert () == CA().popF(0, default=42)
assert (100,) == CA().popF(1, default=100)
```

---

[1]: https://pypi.org/project/grscheller.circular-array
[2]: https://grscheller.github.io/circular-array
[3]: https://github.com/grscheller/circular-array
