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
* generic class with one type parameter

"""

from __future__ import annotations

__version__ = "3.0.0"
__all__ = ['CircularArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from itertools import chain
from typing import Any, Callable, Generic, Iterator, TypeVar

T = TypeVar('T')
S = TypeVar('S')

class CircularArray(Generic[T]):
    """Class implementing an indexable circular array

    * indexing, pushing & popping and length determination all O(1) operations
    * popping from an empty CircularArray returns None
    * in a boolean context returned False if empty, True otherwise
    * iterators caches current content
    * a CircularArray instance will resize itself as needed
    * circularArrays are not sliceable
    * raises: IndexError
    """
    __slots__ = '_count', '_capacity', '_front', '_rear', '_list'

    def __init__(self, *data: T):
        match len(data):
            case 0:
                self._list: list[T|None] = [None, None]
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

    def __iter__(self) -> Iterator[T]:
        if self._count > 0:
            capacity,       rear,       position,    currentState = \
            self._capacity, self._rear, self._front, self._list.copy()

            while position != rear:
                yield currentState[position]            # type: ignore
                position = (position + 1) % capacity
            yield currentState[position]                # type: ignore

    def __reversed__(self) -> Iterator[T]:
        if self._count > 0:
            capacity,       front,       position,   currentState = \
            self._capacity, self._front, self._rear, self._list.copy()

            while position != front:
                yield currentState[position]         # type: ignore
                position = (position - 1) % capacity
            yield currentState[position]             # type: ignore

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return "(|" + ", ".join(map(repr, self)) + "|)"

    def __bool__(self) -> bool:
        return self._count > 0

    def __len__(self) -> int:
        return self._count

    def __getitem__(self, index: int) -> T:
        cnt = self._count
        if 0 <= index < cnt:
            return self._list[(self._front + index) % self._capacity]        # type: ignore
        elif -cnt <= index < 0:
            return self._list[(self._front + cnt + index) % self._capacity]  # type: ignore
        else:
            if cnt > 0:
                msg1 = 'Out of bounds: '
                msg2 = f'index = {index} not between {-cnt} and {cnt-1} '
                msg3 = 'while getting value from a CircularArray.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to get value from an empty CircularArray.'
                raise IndexError(msg0)

    def __setitem__(self, index: int, value: T) -> None:
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

    def __eq__(self, other: object) -> bool:
        """Returns True if all the data stored in both compare as equal.

        * worst case is O(n) behavior for the true case
        * both CircularArrays must be of the same type (contain the same types)
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

    def copy(self) -> CircularArray[T]:
        """Return a shallow copy of the CircularArray."""
        return CircularArray(*self)

    def reverse(self) -> CircularArray[T]:
        """Return a reversed shallow copy of the CircularArray."""
        return CircularArray(*reversed(self))

    def pushR(self, value: T) -> None:
        """Push data onto the rear of the CircularArray."""
        if self._count == self._capacity:
            self.double()
        self._rear = (self._rear + 1) % self._capacity
        self._list[self._rear] = value
        self._count += 1

    def pushL(self, value: T) -> None:
        """Push data onto the front of the CircularArray."""
        if self._count == self._capacity:
            self.double()
        self._front = (self._front - 1) % self._capacity
        self._list[self._front] = value
        self._count += 1

    def popR(self) -> T|None:
        """Pop data off the rear of the CircularArray, returns None if empty."""
        if self._count == 0:
            return None
        else:
            value, self._count, self._list[self._rear], self._rear = \
                self._list[self._rear], self._count-1, None, (self._rear - 1) % self._capacity

            return value

    def popL(self) -> T|None:
        """Pop data off the front of the CircularArray, returns None if empty."""
        if self._count == 0:
            return None
        else:
            value, self._count, self._list[self._front], self._front = \
                self._list[self._front], self._count-1, None, (self._front+1) % self._capacity

            return value

    def map(self, f: Callable[[T], S]) -> CircularArray[S]:
        """Apply function f over the CircularArray's contents and return
        the results in a new CircularArray.
        """
        return CircularArray(*map(f, self))

    def foldL(self, f: Callable[[T, T], T]) -> T|None:
        """Fold CircularArray left.

        * first argument of `f` is the accumulated value
        * if CircularArray is empty, return `None`
        """
        if self._count == 0:
            return None

        iter_self = iter(self)
        value = next(iter_self)

        for v in iter_self:
            value = f(value, v)

        return value

    def foldR(self, f: Callable[[T, T], T]) -> T|None:
        """Fold CircularArray right.

        * second argument of `f` is the accumulated value
        * if CircularArray is empty, return `None`
        """
        if self._count == 0:
            return None

        rev_self = reversed(self)
        value = next(rev_self)
        for v in rev_self:
            value = f(v, value)

        return value

    def foldL1(self, f: Callable[[S, T], S], initial: S) -> S:
        """Fold CircularArray left with an initial value.

        * first argument of `f` is the accumulated value
        * if CircularArray is empty, return the initial value
        """
        if self._count == 0:
            return initial

        value: S = initial
        for v in iter(self):
            value = f(value, v)

        return value

    def foldR1(self, f: Callable[[T, S], S], initial: S) -> S:
        """Fold CircularArray right with an initial value.

        * second argument of `f` is the accumulated value
        * if CircularArray is empty, return the initial value
        """
        if self._count == 0:
            return initial

        value: S = initial
        for v in reversed(self):
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
