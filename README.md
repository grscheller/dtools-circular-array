# Developer Tools - Circular Array

Python package containing a module implementing a circular array data
structure,

- **Repositories**
  - [dtools.circular-array][1] project on *PyPI*
  - [Source code][2] on *GitHub*
- **Detailed documentation**
  - [Detailed API documentation][3] on *GH-Pages*

This project is part of the [Developer Tools for Python][4] **dtools.**
namespace project.

## Overview

- O(1) amortized pushes and pops either end.
- O(1) indexing
- fully supports slicing
- safely mutates while iterating over copies of previous state

### Module circular_array

A full featured, auto resizing circular array. Python package containing
a module implementing a full featured, indexable, sliceable, double
sided, auto-resizing circular array data structure.

Useful either if used directly as an improved version of a Python List
or in a "has-a" relationship when implementing other data structures.

- *module* dtools.circular_array
  - *class* ca: circular array data structure
  - *function* CA: factory function to produce a ca from data

Above nomenclature modeled after of a builtin data type like `list`, where
`ca` takes an optional iterator as an argument and CA is all caps to represent
syntactic sugar like `[]` or `{}`.

#### Usage

```python
    from dtools.circular_array.ca import CA
    
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

______________________________________________________________________

[1]: https://pypi.org/project/dtools.circular-array
[2]: https://github.com/grscheller/dtools-circular-array
[3]: https://grscheller.github.io/dtools-docs/circular-array
[4]: https://github.com/grscheller/dtools-docs
