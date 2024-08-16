# Python Circular Array Implementation

Python module implementing an indexable, double sided,
auto-resizing queue data structure.

* **Repositories**
  * [grscheller.circular-array][1] project on *PyPI*
  * [Source code][2] on *GitHub*
* **Detailed documentation**
  * [Detailed API documentation][3] on *GH-Pages*

### Overview

O(1) indexing and O(1) pushes and pops either end. Useful if used
directly as an improved version of a Python List and in the
implementation of other data structures in a "has-a" relationship.

### Usage

```python
from grscheller.circular_array.ca import CA

ca = CA(1, 2, 3)
assert ca.popL() == 1
assert ca.popR() == 3
ca.pushR(42, 0)
ca.pushL(0, 1)
assert repr(ca) == 'CA(1, 0, 2, 42, 0)'
assert str(ca) == '(|1, 0, 2, 42, 0|)'

ca = CA(*range(1,11))
assert repr(ca) == 'CA(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)'
assert str(ca) == '(|1, 2, 3, 4, 5, 6, 7, 8, 9, 10|)'
assert len(ca) == 10
tup3 = ca.popLT(3)
tup4 = ca.popRT(4)
assert tup3 == (1, 2, 3)
assert tup4 == (10, 9, 8, 7)

assert ca == CA(4, 5, 6)
four, *rest = ca.popFT(1000)
assert four == 4
assert rest == [5, 6]
assert len(ca) == 0

ca = CA(1, 2, 3)
assert ca.popLD(42) == 1
assert ca.popRD(42) == 3
assert ca.popLD(42) == 2
assert ca.popRD(42) == 42
assert ca.popLD(42) == 42
assert len(ca) == 0
```

---

[1]: https://pypi.org/project/grscheller.circular-array
[2]: https://github.com/grscheller/circular-array
[3]: https://grscheller.github.io/circular-array
