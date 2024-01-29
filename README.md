# PyPI grscheller.circular-array Project

Python package containing the CircularArray data structure.

## Overview

The CircularArray class implements an auto-resizing, indexable, double
sided queue data structure. O(1) indexing and O(1) pushes and pops
either end. Useful as an improved version of a Python list. Used in
a has-a relationship by grscheller.datastructure when implementing other
data structures where its functionality is more likely restricted than
augmented.

For detailed API documentation click [here][1].

## Usage

from grscheller.circular_array.circulararray import CircularArray

---

[1]: https://grscheller.github.io/circular-array/API/development/html/grscheller/circular_array/index.html
