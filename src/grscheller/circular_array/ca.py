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

from typing import Callable, cast, Generic, Iterator, Optional, TypeVar
from typing import cast, overload

_D = TypeVar('_D')
_T = TypeVar('_T')
_L = TypeVar('_L')
_R = TypeVar('_R')

class CA(Generic[_D]):
    """Class implementing an indexable circular array.

    * stateful generic data structure that will resize itself as needed
    * amortized O(1) pushing and popping from either end
    * O(1) random access any element
    * make a defensive copy of the data for the purposes of iteration
    * not sliceable
    * in boolean context returns true if not empty, false if empty

    :raises IndexError: For out-of-bounds indexing
    :raises ValueError: For popping from or folding an empty CA

    """
    __slots__ = '_list', '_count', '_capacity', '_front', '_rear'

    def __init__(self, *ds: _D) -> None:
        self._list: list[_D|None] = [None] + list(ds) + [None]
        self._capacity = capacity = len(self._list)
        self._count = capacity - 2
        if capacity == 2:
            self._front = 0
            self._rear = 1
        else:
            self._front = 1
            self._rear = capacity - 2

    def __iter__(self) -> Iterator[_D]:
        if self._count > 0:
            capacity,       rear,       position,    currentState = \
            self._capacity, self._rear, self._front, self._list.copy()

            while position != rear:
                yield cast(_D, currentState[position])  # will always yield a _D
                position = (position + 1) % capacity
            yield cast(_D, currentState[position])  # will always yield a _D

    def __reversed__(self) -> Iterator[_D]:
        if self._count > 0:
            capacity,       front,       position,   currentState = \
            self._capacity, self._front, self._rear, self._list.copy()

            while position != front:
                yield cast(_D, currentState[position])  # will always yield a _D
                position = (position - 1) % capacity
            yield cast(_D, currentState[position])  # will always yield a _D

    def __repr__(self) -> str:
        return 'CA(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return '(|' + ', '.join(map(str, self)) + '|)'

    def __bool__(self) -> bool:
        return self._count > 0

    def __len__(self) -> int:
        return self._count

    def __getitem__(self, index: int) -> _D:
        cnt = self._count
        if 0 <= index < cnt:
            return cast(_D, self._list[(self._front + index)
                                       % self._capacity])  # will always return a _D
        elif -cnt <= index < 0:
            return cast(_D, self._list[(self._front + cnt + index)
                                       % self._capacity])  # will always return a _D
        else:
            if cnt > 0:
                msg1 = 'Out of bounds: '
                msg2 = f'index = {index} not between {-cnt} and {cnt-1} '
                msg3 = 'while getting value from a CA.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to get value from an empty CA.'
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
                msg3 = 'while setting value from a CA.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to set value from an empty CA.'
                raise IndexError(msg0)

    def __eq__(self, other: object) -> bool:
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

    def push_rear(self, *ds: _D) -> None:
        """Push data onto the rear of the CircularArray."""
        for d in ds:
            if self._count == self._capacity:
                self.double()
            self._rear = (self._rear + 1) % self._capacity
            self._list[self._rear] = d
            self._count += 1

    def push_front(self, *ds: _D) -> None:
        """Push data onto the front of the CircularArray."""
        for d in ds:
            if self._count == self._capacity:
                self.double()
            self._front = (self._front - 1) % self._capacity
            self._list[self._front] = d
            self._count += 1

    def pop_front_unsafe(self) -> _D:
        """Pop value from left side (front) of queue.

        :raises ValueError: When called on an empty CA
        """
        if self._count > 0:
            d, \
            self._list[self._front], \
            self._front, \
            self._count \
                = \
            self._list[self._front], \
            None, \
            (self._front+1) % self._capacity, \
            self._count-1
            return cast(_D, d)  # will always yield a _D
        else:
            msg = 'Method pop_front_unsafe called on an empty CA'
            raise ValueError(msg)

    def pop_rear_unsafe(self) -> _D:
        """Pop data off the rear of the CircularArray.

        :return: Removes and returns the value of type _D from end of the CA.
        :raises ValueError: When called on an empty CA.
        """
        if self._count > 0:
            d, \
            self._list[self._rear], \
            self._rear, \
            self._count \
                = \
            self._list[self._rear], \
            None, \
            (self._rear - 1) % self._capacity, \
            self._count-1
            return cast(_D, d)  # will always yield a _D
        else:
            msg = 'Method pop_rear_unsafe called on an empty CA'
            raise ValueError(msg)

    def pop_front(self, num: int=1, default: Optional[_D]=None) -> tuple[_D, ...]:
        """Pop up to n values off the front of the CircularArray.

        * returns a tuple of values popped from the left

        :param num: maximum number of values to return
        :type num: int
        :return: A Tuple[_D, ...] of at most n values of type _D
        """
        ds: list[_D] = []
        while num > 0:
            try:
                popped = self.pop_front_unsafe()
                ds.append(popped)
            except ValueError:
                break
            else:
                num -= 1

        if num == 1 and len(ds) == 0:
            if default is not None:
                ds.append(default)

        return tuple(ds)

    def pop_rear(self, num: int=1, default: Optional[_D]=None) -> tuple[_D, ...]:
        """Pop up to n values off the rear of the CircularArray.

        :param num: maximum number of values to return
        :type num: int
        :param default: value to use when CA is empty and only one value requested
        :type default: _D
        :return: A Tuple[_D, ...] of at most n values of type _D
        """
        ds: list[_D] = []
        n = num
        while n > 0:
            try:
                popped = self.pop_rear_unsafe()
                ds.append(popped)
            except ValueError:
                break
            else:
                n -= 1

        if num == 1 and len(ds) == 0:
            if default is not None:
                ds.append(default)

        return tuple(ds)

    def map(self, f: Callable[[_D], _T]) -> CA[_T]:
        """Apply function f over the CircularArray's contents and return a new
        instance.

        :param f: Generic function of type f[_D, _T] -> CA[_T].
        :return: Returns CA of type CA[_T].
        """
        return CA(*map(f, self))

    def foldL(self, f: Callable[[_L, _D], _L], initial: Optional[_L]=None) -> _L:
        """Left fold CircularArray via a function and an optional initial value.

        :param f: Generic function of type f[_L, _D] -> _L, the first argument
            to f is for the accumulated value.
        :param initial: Optional initial value. Note that if not given then it
            will be the case that _L = _D.
        :type initial: str
        :return: Returns the reduced value of type _L, note that _L and _D can
            be the same type.
        :raises ValueError: When called on an empty CA
        """
        if self._count == 0:
            if initial is None:
                msg = 'Method foldL called on an empty CA without an initial value.'
                raise ValueError(msg)
            else:
                return initial
        else:
            if initial is None:
                acc = cast(_L, self[0])                   # in this case _D = _L
                for idx in range(1, self._count):
                    acc = f(acc, self[idx])
                return acc
            else:
                acc = initial
                for d in self:
                    acc = f(acc, d)
                return acc

    def foldR(self, f: Callable[[_D, _R], _R], initial: Optional[_R]=None) -> _R:
        """Right fold CircularArray via a function and an optional initial value.

        :param f: Generic function of type f[_D, _R] -> _R, the second argument
            to f is for the accumulated value.
        :param initial: Optional initial value. Note that if not given then it
            will be the case that _R = _D.
        :type initial: str
        :return: Returns the reduced value of type _L, note that _L and _D can
            be the same type.
        :raises ValueError: When called on an empty CA
        """
        if self._count == 0:
            if initial is None:
                msg = 'Method foldR called on an empty CA without an initial value.'
                raise ValueError(msg)
            else:
                return initial
        else:
            if initial is None:
                acc = cast(_R, self[-1])                  # in this case _D = _R
                for idx in range(self._count-2, -1, -1):
                    acc = f(self[idx], acc)
                return acc
            else:
                acc = initial
                for d in reversed(self):
                    acc = f(d, acc)
                return acc

    def capacity(self) -> int:
        """Returns current capacity of the CircularArray.

        :return: Return the capacity of the CA[_D].
        :rtype: int
        """
        return self._capacity

    def compact(self) -> None:
        """Compact the CircularArray.

        :rtype: None
        """
        match self._count:
            case 0:
                self._capacity, self._front, self._rear, self._list = \
                2,              0,           1,          [None, None]
            case 1:
                self._capacity, self._front, self._rear, self._list = \
                3,              1,           1,          [None, self._list[self._front], None]
            case _:
                if self._front <= self._rear:
                    self._capacity, self._front, self._rear,  self._list = \
                    self._count+2,  1,           self._count, \
                    [None] + self._list[self._front:self._rear+1] + [None]
                else:
                    self._capacity, self._front, self._rear,  self._list = \
                    self._count+2,  1,           self._count, [None] \
                        + self._list[self._front:] + self._list[:self._rear+1] \
                        + [None]

    def double(self) -> None:
        """Double the capacity of the CircularArray.

        :rtype: None
        """
        if self._front <= self._rear:
            self._list += [None]*self._capacity
            self._capacity *= 2
        else:
            self._list = self._list[:self._front] + [None]*self._capacity + self._list[self._front:]
            self._front += self._capacity
            self._capacity *= 2

    def empty(self) -> None:
        """Empty the CircularArray, keep current capacity.

        :rtype: None
        """
        self._list, self._front, self._rear = [None]*self._capacity, 0, self._capacity-1

    def fractionFilled(self) -> float:
        """Returns fractional capacity of the CircularArray.

        :rtype: float
        """
        return self._count/self._capacity

    def resize(self, newSize: int= 0) -> None:
        """Compact CircularArray and resize to newSize if less than newSize.

        :param newSize: desired minimal size of the CA[_D]
        :rtype: None
        """
        self.compact()
        capacity = self._capacity
        if newSize > capacity:
            self._list, self._capacity = self._list+[None]*(newSize-capacity), newSize
            if self._count == 0:
                self._rear = capacity - 1
