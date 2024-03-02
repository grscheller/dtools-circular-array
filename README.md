# PyPI grscheller.circular-array Project

Circular Array

* Python module implementing an indexable, double sided queue
* See [grscheller.circular-array][1] project on PyPI
* See [Detailed API documentation][2] on GH-Pages
* See [Source code][3] on GitHub

## Overview

The CircularArray class implements an auto-resizing, indexable, double
sided queue data structure. O(1) indexing and O(1) pushes and pops
either end. Useful as an improved version of a Python list. Used in
a has-a relationship by grscheller.datastructure when implementing other
data structures where its functionality was more likely restricted than
augmented.

## Usage

from grscheller.circular_array import CircularArray

---

[1]: https://pypi.org/project/grscheller.circular-array
[2]: https://grscheller.github.io/circular-array
[3]: https://github.com/grscheller/circular-array
