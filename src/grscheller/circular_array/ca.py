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

"""### Indexable circular array data structure module."""
from __future__ import annotations
from collections.abc import Callable, Iterable, Iterator, Sequence
from typing import Any, cast, Never, overload

__all__ = ['ca', 'CA']

class ca[D](Sequence[D]):
    """
    #### Indexable circular array data structure

    * generic, stateful data structure
    * amortized O(1) pushing and popping from either end
    * O(1) random access any element
    * will resize itself as needed
    * makes defensive copies of contents for the purposes of iteration
    * not sliceable
    * in boolean context returns true if not empty, false if empty
    * in comparisons compare identity before equality (like Python built-ins do)
      * as Python tuples, lists, and dicts do
    * raises `IndexError` for out-of-bounds indexing
    * raises `ValueError` for popping from or folding an empty `ca`
    * raises `TypeError` if more than 2 arguments are passed to constructor

    """
    __slots__ = '_data', '_count', '_capacity', '_front', '_rear'

    def __init__(self, *dss: Iterable[D]) -> None:
        if len(dss) < 2:
            self._data: list[D|None] = [None] + cast(list[D|None], list(*dss)) + [None]
        else:
            msg = f'ca expected at most 1 argument, got {len(dss)}'
            raise TypeError(msg)
        self._capacity = capacity = len(self._data)
        self._count = capacity - 2
        if capacity == 2:
            self._front = 0
            self._rear = 1
        else:
            self._front = 1
            self._rear = capacity - 2

    def _double_storage_capacity(self) -> None:
        if self._front <= self._rear:
            self._data += [None]*self._capacity
            self._capacity *= 2
        else:
            self._data = self._data[:self._front] + [None]*self._capacity + self._data[self._front:]
            self._front, self._capacity = self._front + self._capacity, 2*self._capacity

    def _compact_storage_capacity(self) -> None:
        """Compact the ca."""
        match self._count:
            case 0:
                self._capacity, self._front, self._rear, self._data = 2, 0, 1, [None, None]
            case 1:
                self._capacity, self._front, self._rear, self._data = 3, 1, 1, [None, self._data[self._front], None]
            case _:
                if self._front <= self._rear:
                    self._capacity, self._front, self._rear, self._data = \
                        self._count+2, 1, self._count, [None] + self._data[self._front:self._rear+1] + [None]
                else:
                    self._capacity, self._front, self._rear, self._data = \
                        self._count+2, 1, self._count, [None] + self._data[self._front:] + self._data[:self._rear+1] + [None]

    def __iter__(self) -> Iterator[D]:
        if self._count > 0:
            capacity, rear, position, current_state = \
                self._capacity, self._rear, self._front, self._data.copy()

            while position != rear:
                yield cast(D, current_state[position])
                position = (position + 1) % capacity
            yield cast(D, current_state[position])

    def __reversed__(self) -> Iterator[D]:
        if self._count > 0:
            capacity, front, position, current_state = \
                self._capacity, self._front, self._rear, self._data.copy()

            while position != front:
                yield cast(D, current_state[position])
                position = (position - 1) % capacity
            yield cast(D, current_state[position])

    def __repr__(self) -> str:
        return 'CA(' + ', '.join(map(repr, self)) + ')'

    def __str__(self) -> str:
        return '(|' + ', '.join(map(str, self)) + '|)'

    def __bool__(self) -> bool:
        return self._count > 0

    def __len__(self) -> int:
        return self._count

    @overload
    def __getitem__(self, index: int, /) -> D: ...
    @overload
    def __getitem__(self, slicei: slice, /) -> ca[D]: ...

    def __getitem__(self, idx: int|slice, /) -> D|ca[D]|Never:
        if isinstance(idx, slice):
            raise NotImplementedError

        cnt = self._count
        if 0 <= idx < cnt:
            return cast(D, self._data[(self._front + idx) % self._capacity])
        elif -cnt <= idx < 0:
            return cast(D, self._data[(self._front + cnt + idx) % self._capacity])
        else:
            if cnt > 0:
                msg1 = 'Out of bounds: '
                msg2 = f'index = {idx} not between {-cnt} and {cnt-1} '
                msg3 = 'while getting value from a ca.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to get a value from an empty ca.'
                raise IndexError(msg0)

    def __setitem__(self, index: int, value: D, /) -> None:
        cnt = self._count
        if 0 <= index < cnt:
            self._data[(self._front + index) % self._capacity] = value
        elif -cnt <= index < 0:
            self._data[(self._front + cnt + index) % self._capacity] = value
        else:
            if cnt > 0:
                msg1 = 'Out of bounds: '
                msg2 = f'index = {index} not between {-cnt} and {cnt-1} '
                msg3 = 'while setting value from a ca.'
                raise IndexError(msg1 + msg2 + msg3)
            else:
                msg0 = 'Trying to set a value from an empty ca.'
                raise IndexError(msg0)

    def __eq__(self, other: object, /) -> bool:
        if self is other:
            return True
        if not isinstance(other, type(self)):
            return False

        frontL, frontR, \
        countL, countR, \
        capacityL, capacityR = \
            self._front, other._front, \
            self._count, other._count, \
            self._capacity, other._capacity

        if countL != countR:
            return False

        for nn in range(countL):
            if self._data[(frontL+nn)%capacityL] is other._data[(frontR+nn)%capacityR]:
                continue
            if self._data[(frontL+nn)%capacityL] != other._data[(frontR+nn)%capacityR]:
                return False
        return True

    def pushL(self, *ds: D) -> None:
        """Push data from the left onto the ca."""
        for d in ds:
            if self._count == self._capacity:
                self._double_storage_capacity()
            self._front = (self._front - 1) % self._capacity
            self._data[self._front], self._count = d, self._count + 1

    def pushR(self, *ds: D) -> None:
        """Push data from the right onto the ca."""
        for d in ds:
            if self._count == self._capacity:
                self._double_storage_capacity()
            self._rear = (self._rear + 1) % self._capacity
            self._data[self._rear], self._count = d, self._count + 1

    def popL(self) -> D|Never:
        """Pop one value off the left side of the ca.

        * raises `ValueError` when called on an empty ca
        """
        if self._count > 1:
            d, self._data[self._front], self._front, self._count = \
                self._data[self._front], None, (self._front+1) % self._capacity, self._count - 1
        elif self._count < 1:
            msg = 'Method popL called on an empty ca'
            raise ValueError(msg)
        else:
            d, self._data[self._front], self._count, self._front, self._rear = \
                self._data[self._front], None, 0, 0, self._capacity - 1
        return cast(D, d)

    def popR(self) -> D|Never:
        """Pop one value off the right side of the ca.

        * raises `ValueError` when called on an empty ca
        """
        if self._count > 0:
            d, self._data[self._rear], self._rear, self._count = \
                self._data[self._rear], None, (self._rear - 1) % self._capacity, self._count - 1
        elif self._count < 1:
            msg = 'Method popR called on an empty ca'
            raise ValueError(msg)
        else:
            d, self._data[self._front], self._count, self._front, self._rear = \
                self._data[self._front], None, 0, 0, self._capacity - 1
        return cast(D, d)

    def popLD(self, default: D, /) -> D:
        """Pop one value from left, provide a mandatory default value.

        * safe version of popL
        * returns a default value in the event the `ca` is empty
        """
        try:
            return self.popL()
        except ValueError:
            return default

    def popRD(self, default: D, /) -> D:
        """Pop one value from right, provide a mandatory default value.

        * safe version of popR
        * returns a default value in the event the `ca` is empty
        """
        try:
            return self.popR()
        except ValueError:
            return default

    def popLT(self, max: int) -> tuple[D, ...]:
        """Pop multiple values from left side of ca.

        * returns the results in a tuple of type `tuple[~D, ...]`
        * returns an empty tuple if `ca` is empty
        * pop no more that `max` values
        * will pop less if `ca` becomes empty
        """
        ds: list[D] = []

        while max > 0:
            try:
                ds.append(self.popL())
            except ValueError:
                break
            else:
                max -= 1

        return tuple(ds)

    def popRT(self, max: int) -> tuple[D, ...]:
        """Pop multiple values from right side of `ca`.

        * returns the results in a tuple of type `tuple[~D, ...]`
        * returns an empty tuple if `ca` is empty
        * pop no more that `max` values
        * will pop less if `ca` becomes empty
        """
        ds: list[D] = []
        while max > 0:
            try:
                ds.append(self.popR())
            except ValueError:
                break
            else:
                max -= 1

        return tuple(ds)

    def map[U](self, f: Callable[[D], U], /) -> ca[U]:
        """Apply function f over contents, returns new `ca` instance.

        * parameter `f` function of type `f[~D, ~U] -> ca[~U]`
        * returns a new instance of type `ca[~U]`
        """
        return ca(map(f, self))

    def foldL[L](self, f: Callable[[L, D], L], /, initial: L|None=None) -> L:
        """Left fold ca via function and optional initial value.

        * parameter `f` function of type `f[~L, ~D] -> ~L`
          * the first argument to `f` is for the accumulated value.
        * parameter `initial` is an optional initial value
        * returns the reduced value of type `~L`
          * note that `~L` and `~D` can be the same type
          * if an initial value is not given then by necessity `~L = ~D`
        * raises `ValueError` when called on an empty `ca` and `initial` not given
        """
        if self._count == 0:
            if initial is None:
                msg = 'Method foldL called on an empty ca without an initial value.'
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

    def foldR[R](self, f: Callable[[D, R], R], /, initial: R|None=None) -> R:
        """Right fold ca via function and optional initial value.

        * parameter `f` function of type `f[~D, ~R] -> ~R`
          * the second argument to f is for the accumulated value
        * parameter `initial` is an optional initial value
        * returns the reduced value of type `~R`
          * note that `~R` and `~D` can be the same type
          * if an initial value is not given then by necessity `~R = ~D`
        * raises `ValueError` when called on an empty `ca` and `initial` not given
        """
        if self._count == 0:
            if initial is None:
                msg = 'Method foldR called on an empty ca without an initial value.'
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
        """Returns current capacity of the ca."""
        return self._capacity

    def empty(self) -> None:
        """Empty the ca, keep current capacity."""
        self._data, self._front, self._rear = [None]*self._capacity, 0, self._capacity-1

    def fractionFilled(self) -> float:
        """Returns fractional capacity of the ca."""
        return self._count/self._capacity

    def resize(self, min_capacity: int=2) -> None:
        """Compact `ca` and resize to `min_capacity` if necessary.

        * to just compact the `ca`, do not provide a min_capacity
        """
        self._compact_storage_capacity()
        if min_capacity > self._capacity:
            self._capacity, self._data = \
                min_capacity, self._data + [None]*(min_capacity-self._capacity)
            if self._count == 0:
                self._front, self._rear = 0, self._capacity - 1

def CA[U](*ds: U) -> ca[U]:
    """Function to produce a `ca` array from a variable number of arguments."""
    return ca(ds)
