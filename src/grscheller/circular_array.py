# Copyright 2023-2024 Geoffrey R. Scheller
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Module for an indexable circular array data structure.

* stateful data structure
* O(1) random access any element
* amortized O(1) pushing and popping from either end
* data structure will resize itself as needed

"""

from __future__ import annotations

__version__ = "2.0.0"
__all__ = ['CircularArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Any, Callable
from itertools import chain

class CircularArray:
    """Class implementing an indexible circular array

    * indexing, pushing & popping and length determination all O(1) operations
    * popping from an empty CircularArray returns None
    * in a boolean context returnd False if empty, True otherwise
    * iterators caches current content
    * a CircularArray instance will resize itself as needed
    * circularArrays are not sliceable
    * raises: IndexError
    """
    __slots__ = '_count', '_capacity', '_front', '_rear', '_list'

    def __init__(self, *data):
        match len(data):
            case 0:
                self._list = [None, None]
                self._count = 0
                self._capacity = 2
                self._front = 0
                self._rear = 1
            case count:
                self._list = list(data)
                self._count = count
                self._capacity = count
                self._front = 0
                self._rear = count - 1

    def __iter__(self):
        if self._count > 0:
            capacity,       rear,       position,    currentState = \
            self._capacity, self._rear, self._front, self._list.copy()

            while position != rear:
                yield currentState[position]
                position = (position + 1) % capacity
            yield currentState[position]

    def __reversed__(self):
        if self._count > 0:
            capacity,       front,       position,   currentState = \
            self._capacity, self._front, self._rear, self._list.copy()

            while position != front:
                yield currentState[position]
                position = (position - 1) % capacity
            yield currentState[position]

    def __repr__(self):
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, self)) + ')'

    def __str__(self):
        return "(|" + ", ".join(map(repr, self)) + "|)"

    def __bool__(self):
        return self._count > 0

    def __len__(self):
        return self._count

    def __getitem__(self, index: int) -> Any:
        cnt = self._count
        if 0 <= index < cnt:
            return self._list[(self._front + index) % self._capacity]
        elif -cnt <= index < 0:
            return self._list[(self._front + cnt + index) % self._capacity]
        else:
            if cnt > 0:
                msg1 = 'Out of bounds: '
                msg2 = f'index = {index} not between {-cnt} and {cnt-1} '
                msg3 = 'while getting value from a CircularArray.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to get value from an empty CircularArray.'
                raise IndexError(msg0)

    def __setitem__(self, index: int, value: Any) -> Any:
        cnt = self._count
        if 0 <= index < cnt:
            self._list[(self._front + index) % self._capacity] = value
        elif -cnt <= index < 0:
            self._list[(self._front + cnt + index) % self._capacity] = value
        else:
            if cnt > 0:
                msg1 = 'Out of bounds: '
                msg2 = f'index = {index} not between {-cnt} and {cnt-1} '
                msg3 = 'while setting value from a CircularArray.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to set value from an empty CircularArray.'
                raise IndexError(msg0)

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False

        frontL,      capacityL,      countL,      frontR,       capacityR,       countR = \
        self._front, self._capacity, self._count, other._front, other._capacity, other._count

        if countL != countR:
            return False

        for nn in range(countL):
            if self._list[(frontL+nn)%capacityL] != other._list[(frontR+nn)%capacityR]:
                return False
        return True

    def copy(self) -> CircularArray:
        """Return a shallow copy of the CircularArray."""
        return CircularArray(*self)

    def reverse(self) -> CircularArray:
        return CircularArray(*reversed(self))

    def pushR(self, value: Any) -> None:
        """Push data onto the rear of the CircularArray."""
        if self._count == self._capacity:
            self.double()
        self._rear = (self._rear + 1) % self._capacity
        self._list[self._rear] = value
        self._count += 1

    def pushL(self, value: Any) -> None:
        """Push data onto the front of the CircularArray."""
        if self._count == self._capacity:
            self.double()
        self._front = (self._front - 1) % self._capacity
        self._list[self._front] = value
        self._count += 1

    def popR(self) -> Any:
        """Pop data off the rear of the CirclularArray, returns None if empty."""
        if self._count == 0:
            return None
        else:
            value, self._count, self._list[self._rear], self._rear = \
                self._list[self._rear], self._count-1, None, (self._rear - 1) % self._capacity

            return value

    def popL(self) -> Any:
        """Pop data off the front of the CirclularArray, returns None if empty."""
        if self._count == 0:
            return None
        else:
            value, self._count, self._list[self._front], self._front = \
                self._list[self._front], self._count-1, None, (self._front+1) % self._capacity

            return value

    def map(self, f: Callable[[Any], Any]) -> CircularArray:
        """Apply function f over the CircularArray's contents and return
        the results in a new CircularArray.
        """
        return CircularArray(*map(f, self))

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Apply function f over the CircularArray's contents mutating the
        CircularArray, does not return anything.
        """
        ca  = CircularArray(*map(f, self))

        self._count, self._capacity, self._front, self._rear, self._list = \
        ca._count,   ca._capacity,   ca._front,   ca._rear,   ca._list

    def foldL(self, f: Callable[[Any, Any], Any], initial: Any=None) -> Any:
        """Fold left with optional initial value. The first argument of `f` is
        the accumulated value. If CircularArray is empty and no initial value
        given, return `None`.
        """
        if self._count == 0:
            return initial
        
        if initial is None:
            vs = iter(self)
        else:
            vs = chain((initial,), self)

        value = next(vs)
        for v in vs:
            value = f(value, v)

        return value

    def foldR(self, f: Callable[[Any, Any], Any], initial: Any=None) -> Any:
        """Fold right with optional initial value. The second argument of `f` is
        the accumulated value. If CircularArray is empty and no initial
        value given, return `None`.
        """
        if self._count == 0:
            return initial
        
        if initial is None:
            vs = reversed(self)
        else:
            vs = chain((initial,), reversed(self))

        value = next(vs)
        for v in vs:
            value = f(v, value)

        return value

    def capacity(self) -> int:
        """Returns current capacity of the CircularArray."""
        return self._capacity

    def compact(self) -> None:
        """Compact the CircularArray as much as possible."""
        match self._count:
            case 0:
                self._capacity, self._front, self._rear, self._list = 2, 0, 1, [None]*2 
            case 1:
                self._capacity, self._front, self._rear, self._list = 1, 0, 0, [self._list[self._front]] 
            case _:
                if self._front <= self._rear:
                    self._capacity, self._front, self._rear,    self._list = \
                    self._count,    0,           self._count-1, self._list[self._front:self._rear+1]
                else:
                    self._capacity, self._front, self._rear,    self._list = \
                    self._count,    0,           self._count-1, self._list[self._front:] + self._list[:self._rear+1]

    def double(self) -> None:
        """Double the capacity of the CircularArray."""
        if self._front <= self._rear:
            self._list += [None]*self._capacity
            self._capacity *= 2
        else:
            self._list = self._list[:self._front] + [None]*self._capacity + self._list[self._front:]
            self._front += self._capacity
            self._capacity *= 2

    def empty(self) -> None:
        """Empty the CircularArray, keep current capacity."""
        self._list, self._front, self._rear = [None]*self._capacity, 0, self._capacity-1

    def fractionFilled(self) -> float:
        """Returns fractional capacity of the CircularArray."""
        return self._count/self._capacity

    def resize(self, newSize: int= 0) -> None:
        """Compact CircularArray and resize to newSize if less than newSize."""
        self.compact()
        capacity = self._capacity
        if newSize > capacity:
            self._list, self._capacity = self._list+[None]*(newSize-capacity), newSize
            if self._count == 0:
                self._rear = capacity - 1

if __name__ == "__main__":
    pass
