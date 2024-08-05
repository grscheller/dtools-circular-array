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

D = TypeVar('D')
T = TypeVar('T')
L = TypeVar('L')
R = TypeVar('R')

class CA(Generic[D]):
    """Class implementing an indexable circular array.

    * stateful generic data structure that will resize itself as needed
    * amortized O(1) pushing and popping from either end
    * O(1) random access any element
    * make a defensive copy of the data for the purposes of iteration
    * not sliceable
    * in boolean context returns true if not empty, false if empty
    * raises `IndexError` for out-of-bounds indexing
    * raises `ValueError` for popping from or folding an empty CA

    """
    __slots__ = '_list', '_count', '_capacity', '_front', '_rear'

    def __init__(self, *ds: D) -> None:
        self._list: list[D|None] = [None] + list(ds) + [None]
        self._capacity = capacity = len(self._list)
        self._count = capacity - 2
        if capacity == 2:
            self._front = 0
            self._rear = 1
        else:
            self._front = 1
            self._rear = capacity - 2

    def __iter__(self) -> Iterator[D]:
        if self._count > 0:
            capacity,       rear,       position,    currentState = \
            self._capacity, self._rear, self._front, self._list.copy()

            while position != rear:
                yield cast(D, currentState[position])  # will always yield a D
                position = (position + 1) % capacity
            yield cast(D, currentState[position])  # will always yield a D

    def __reversed__(self) -> Iterator[D]:
        if self._count > 0:
            capacity,       front,       position,   currentState = \
            self._capacity, self._front, self._rear, self._list.copy()

            while position != front:
                yield cast(D, currentState[position])  # will always yield a D
                position = (position - 1) % capacity
            yield cast(D, currentState[position])  # will always yield a D

    def __repr__(self) -> str:
        return 'CA(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return '(|' + ', '.join(map(str, self)) + '|)'

    def __bool__(self) -> bool:
        return self._count > 0

    def __len__(self) -> int:
        return self._count

    def __getitem__(self, index: int) -> D:
        cnt = self._count
        if 0 <= index < cnt:
            return cast(D, self._list[(self._front + index)
                                       % self._capacity])  # will always return a D
        elif -cnt <= index < 0:
            return cast(D, self._list[(self._front + cnt + index)
                                       % self._capacity])  # will always return a D
        else:
            if cnt > 0:
                msg1 = 'Out of bounds: '
                msg2 = f'index = {index} not between {-cnt} and {cnt-1} '
                msg3 = 'while getting value from a CA.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to get value from an empty CA.'
                raise IndexError(msg0)

    def __setitem__(self, index: int, value: D) -> None:
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

    def push_front(self, *ds: D) -> None:
        """Push data onto the front of the CircularArray."""
        for d in ds:
            if self._count == self._capacity:
                self.double()
            self._front = (self._front - 1) % self._capacity
            self._list[self._front] = d
            self._count += 1

    def push_rear(self, *ds: D) -> None:
        """Push data onto the rear of the CircularArray."""
        for d in ds:
            if self._count == self._capacity:
                self.double()
            self._rear = (self._rear + 1) % self._capacity
            self._list[self._rear] = d
            self._count += 1

    def pop_front_unsafe(self) -> D:
        """Pop value from front ("left side") of CircularArray.

        * returns and removes a value of type D from the front of the CA
        * raises `ValueError` when called on an empty CA

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
            return cast(D, d)  # will always yield a D
        else:
            msg = 'Method pop_front_unsafe called on an empty CA'
            raise ValueError(msg)

    def pop_rear_unsafe(self) -> D:
        """Pop data off the rear ("right side") of the CircularArray.

        * returns and removes a value of type D from the rear of the CA
        * raises `ValueError` when called on an empty CA

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
            return cast(D, d)  # will always yield a D
        else:
            msg = 'Method pop_rear_unsafe called on an empty CA'
            raise ValueError(msg)

    def pop_front(self, num: int=1, default: Optional[D]=None) -> tuple[D, ...]:
        """Pop up to `num` values off the front of the CircularArray.

        * parameter `num` is the maximum number of values to return
        * parameter `default` is used when CA is empty and only one value requested
        * returns a `Tuple[D, ...]` of at most `num` values popped from front of CA

        """
        ds: list[D] = []
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

    def pop_rear(self, num: int=1, default: Optional[D]=None) -> tuple[D, ...]:
        """Pop up to `num` values off the rear of the CircularArray.

        * parameter `num` is the maximum number of values to return
        * parameter `default` is used when CA is empty and only one value requested
        * returns a `Tuple[D, ...]` of at most `num` values popped from rear of CA

        """
        ds: list[D] = []
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

    def map(self, f: Callable[[D], T]) -> CA[T]:
        """Apply function f over the CA's contents and return new instance.

        * parameter `f` generic function of type f[D, T] -> CA[T]
        * return a new instance of a CA of type CA[T]

        """
        return CA(*map(f, self))

    def foldL(self, f: Callable[[L, D], L], initial: Optional[L]=None) -> L:
        """Left fold CircularArray via a function and an optional initial value.

        * parameter `f` generic function of type `f[L, D] -> L`
          * the first argument to `f` is for the accumulated value.
        * parameter `initial` is an optional initial value
          * note that if not given then it will be the case that `L` = `D`
        * returns the reduced value of type `L`
          * note that `L` & `D` can be the same type
          * if `initial` is not given then `L = R`
        * raises `ValueError` when called on an empty CA

        """
        if self._count == 0:
            if initial is None:
                msg = 'Method foldL called on an empty CA without an initial value.'
                raise ValueError(msg)
            else:
                return initial
        else:
            if initial is None:
                acc = cast(L, self[0])  # in this case D = L
                for idx in range(1, self._count):
                    acc = f(acc, self[idx])
                return acc
            else:
                acc = initial
                for d in self:
                    acc = f(acc, d)
                return acc

    def foldR(self, f: Callable[[D, R], R], initial: Optional[R]=None) -> R:
        """Right fold CircularArray via a function and an optional initial value.

        * parameter `f` generic function of type `f[D, R] -> R`
          * the second argument to f is for the accumulated value
        * parameter `initial` is an optional initial value
          * note that if not given then it will be the case that `R` = `D`
        * returns the reduced value of type `R`
          * note that `R` & `D` can be the same type
          * if `initial` is not given then `L = R`
        * raises `ValueError` when called on an empty CA

        """
        if self._count == 0:
            if initial is None:
                msg = 'Method foldR called on an empty CA without an initial value.'
                raise ValueError(msg)
            else:
                return initial
        else:
            if initial is None:
                acc = cast(R, self[-1])  # in this case D = R
                for idx in range(self._count-2, -1, -1):
                    acc = f(self[idx], acc)
                return acc
            else:
                acc = initial
                for d in reversed(self):
                    acc = f(d, acc)
                return acc

    def capacity(self) -> int:
        """Returns current capacity of the CircularArray."""
        return self._capacity

    def compact(self) -> None:
        """Compact the CircularArray."""
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
