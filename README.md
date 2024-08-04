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

ca = CA(1, 2, 3, s=None)
assert ca.popL() == 1
assert ca.popR() == 3
ca.pushR(42, 0)
assert repr(ca) == 'CA(2, 42, 0, s=None)'
assert str(ca) == '(|2, 42, 0|:None)'
assert ca.popL() == 2
assert ca.popL() == 42
assert ca.popL() == 0
assert ca.popL() == None

ca0 = CA(1, 2, s=0)
assert ca0.popR() == 2
assert ca0.popR() == 1
assert ca0.popR() == 0
```

---

[1]: https://pypi.org/project/grscheller.circular-array
[2]: https://grscheller.github.io/circular-array
[3]: https://github.com/grscheller/circular-array
