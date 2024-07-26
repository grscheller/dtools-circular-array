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

"""Module for an indexable circular array data structure."""

from __future__ import annotations

__all__ = ['CA']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Apache License 2.0"

from typing import Callable, Generic, Iterator, Optional, TypeVar

_D = TypeVar('_D')
_S = TypeVar('_S')
_L = TypeVar('_L')
_R = TypeVar('_R')
_U = TypeVar('_U')

class CA(Generic[_D, _S]):
    """Class implementing an indexable circular array

    * stateful generic data structure with a data type and a "fallback/sentinel" type
    * amortized O(1) pushing and popping from either end
    * O(1) random access any element
    * will resize itself as needed
    * not sliceable
    * in a boolean context returned False if empty, True otherwise
    * intended to implement other data structures, so
    * does not make defensive copies of data for the purposes of iteration
    * raises: IndexError

    """
    __slots__ = '_count', '_capacity', '_front', '_rear', '_list', '_s'

    def __init__(self, *ds: _D, sentinel: _S):
        self._s = sentinel
        match len(ds):
            case 0:
                self._list: list[_D|_S] = [sentinel, sentinel]
                self._count = 0
                self._capacity = 2
                self._front = 0
                self._rear = 1
            case count:
                self._list = list(ds)
                self._count = count
                self._capacity = count
                self._front = 0
                self._rear = count - 1

    def __iter__(self) -> Iterator[_D]:
        if self._count > 0:
            capacity,       rear,       position,    currentState = \
            self._capacity, self._rear, self._front, self._list.copy()

            while position != rear:
                yield currentState[position]          # type: ignore # will always yield _D
                position = (position + 1) % capacity
            yield currentState[position]              # type: ignore # will always yield _D

    def __reversed__(self) -> Iterator[_D]:
        if self._count > 0:
            capacity,       front,       position,   currentState = \
            self._capacity, self._front, self._rear, self._list.copy()

            while position != front:
                yield currentState[position]         # type: ignore # will always yield _D
                position = (position - 1) % capacity
            yield currentState[position]             # type: ignore # will always yield _D

    def __repr__(self) -> str:
        return 'CA(' + ', '.join(map(repr, self)) + ', sentinel = ' + repr(self._s) + ')'

    def __str__(self) -> str:
        return "(|" + ", ".join(map(str, self)) + "|)"

    def __bool__(self) -> bool:
        return self._count > 0

    def __len__(self) -> int:
        return self._count

    def __getitem__(self, index: int) -> _D:
        cnt = self._count
        if 0 <= index < cnt:
            return self._list[(self._front + index) % self._capacity]        # type: ignore # will always return a _D
        elif -cnt <= index < 0:
            return self._list[(self._front + cnt + index) % self._capacity]  # type: ignore # will always return a _D
        else:
            if cnt > 0:
                msg1 = 'Out of bounds: '
                msg2 = f'index = {index} not between {-cnt} and {cnt-1} '
                msg3 = 'while getting value from a CircularArray.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to get value from an empty CircularArray.'
                raise IndexError(msg0)

    def __setitem__(self, index: int, value: _D) -> None:
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

        """
        if not isinstance(other, type(self)):
            return False
        if self._s != other._s:
            return False

        frontL,      capacityL,      countL,      frontR,       capacityR,       countR = \
        self._front, self._capacity, self._count, other._front, other._capacity, other._count

        if countL != countR:
            return False

        for nn in range(countL):
            if self._list[(frontL+nn)%capacityL] != other._list[(frontR+nn)%capacityR]:
                return False
        return True

    def copy(self) -> CA[_D, _S]:
        """Return a shallow copy of the CircularArray."""
        return CA(*self, sentinel=self._s)

    def pushR(self, *ds: _D) -> None:
        """Push data onto the rear of the CircularArray."""
        for d in ds:
            if self._count == self._capacity:
                self.double()
            self._rear = (self._rear + 1) % self._capacity
            self._list[self._rear] = d
            self._count += 1

    def pushL(self, *ds: _D) -> None:
        """Push data onto the front of the CircularArray."""
        for d in ds:
            if self._count == self._capacity:
                self.double()
            self._front = (self._front - 1) % self._capacity
            self._list[self._front] = d
            self._count += 1

    def popR(self) -> _D|_S:
        """Pop data off the rear of the CircularArray.

        * returns None if empty
        * use in a boolean context to determine if empty

        """
        if self._count == 0:
            return self._s
        else:
            d, self._count, self._list[self._rear], self._rear = \
                self._list[self._rear], self._count-1, self._s, (self._rear - 1) % self._capacity
            return d

    def popL(self) -> _D|_S:
        """Pop data off the front of the CircularArray.

        * returns None if empty
        * use in a boolean context to determine if empty

        """
        if self._count == 0:
            return self._s
        else:
            d, self._count, self._list[self._front], self._front = \
                self._list[self._front], self._count-1, self._s, (self._front+1) % self._capacity
            return d

    def map(self, f: Callable[[_D], _U]) -> CA[_U, _S]:
        """Apply function f over the CircularArray's contents.

        * return the results in a new CircularArray

        """
        return CA(*map(f, self), sentinel=self._s)

    def foldL(self, f: Callable[[_D, _D], _D]) -> _D|_S:
        """Fold left with an initial value.

        * first argument of function f is for the accumulated value
        * if empty, return the sentinel value of type _S

        """
        if self:
            it = iter(self)
            acc = next(it)
            for v in it:
                acc = f(acc, v)
            return acc
        else:
            return self._s

    def foldL1(self, f: Callable[[_L, _D], _L], init: _L) -> _L:
        """Fold left with an initial value.

        * first argument of function f is for the accumulated value

        """
        acc = init
        for v in iter(self):
            acc = f(acc, v)
        return acc

    def foldR(self, f: Callable[[_D, _D], _D]) -> _D|_S:
        """Fold right with an initial value.

        * second argument of function f is for the accumulated value
        * if empty, return the sentinel value of type _S

        """
        if self:
            it = reversed(self)
            acc = next(it)
            for v in it:
                acc = f(v, acc)
            return acc
        else:
            return self._s

    def foldR1(self, f: Callable[[_D, _R], _R], init: _R) -> _R:
        """Fold right with an initial value.

        * second argument of function f is for the accumulated value

        """
        acc = init
        for v in reversed(self):
            acc = f(v, acc)
        return acc

    def capacity(self) -> int:
        """Returns current capacity of the CircularArray."""
        return self._capacity

    def compact(self) -> None:
        """Compact the CircularArray as much as possible."""
        match self._count:
            case 0:
                self._capacity, self._front, self._rear, self._list = 2, 0, 1, [self._s]*2
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
            self._list += [self._s]*self._capacity
            self._capacity *= 2
        else:
            self._list = self._list[:self._front] + [self._s]*self._capacity + self._list[self._front:]
            self._front += self._capacity
            self._capacity *= 2

    def empty(self) -> None:
        """Empty the CircularArray, keep current capacity."""
        self._list, self._front, self._rear = [self._s]*self._capacity, 0, self._capacity-1

    def fractionFilled(self) -> float:
        """Returns fractional capacity of the CircularArray."""
        return self._count/self._capacity

    def resize(self, newSize: int= 0) -> None:
        """Compact CircularArray and resize to newSize if less than newSize."""
        self.compact()
        capacity = self._capacity
        if newSize > capacity:
            self._list, self._capacity = self._list+[self._s]*(newSize-capacity), newSize
            if self._count == 0:
                self._rear = capacity - 1
