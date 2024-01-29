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

"""Module grscheller.circulararray.circulararray - circlar array datastructure

Module implementing a stateful circular array data structures with amortized O(1)
pushing and popping from either end and O(1) indexing. Implemented with a Python List,
this data structure will resize itself as needed.
"""

from __future__ import annotations

__all__ = ['CircularArray']
__author__ = "Geoffrey R. Scheller"
__copyright__ = "Copyright (c) 2023-2024 Geoffrey R. Scheller"
__license__ = "Appache License 2.0"

from typing import Any, Callable

class CircularArray:
    """An auto-resizing, indexable, double sided queue data structure. O(1) indexing
    and O(1) pushes and pops either end. Useful as an improved version of a Python list.
    Used in a has-a relationship by grscheller.datastructure when implementing other
    data structures where its functionality is more likely restricted than augmented.

    Note: Indexing, pushing & popping and size determination are all O(1) operations
    Note: Popping from an empty Circulararray returns None
    Note: Use in a boolean context to determine if empty
    Note: A Circulararray will resize itself as needed
    Note: For now, Circulararrays are not sliceable

    Raises: IndexError
    """
    __slots__ = '_count', '_capacity', '_front', '_rear', '_list'

    def __init__(self, *data):
        """Construct a double sided queue"""
        size = len(data)
        capacity = size + 2
        self._count = size
        self._capacity = capacity
        self._front = 0
        self._rear = (size - 1) % capacity
        self._list = list(data)
        self._list.append(None)
        self._list.append(None)

    def __iter__(self):
        """Generator yielding the cached contents of the current state of
        the CircularArray.
        """
        if self._count > 0:
            cap = self._capacity
            rear = self._rear
            pos = self._front
            currList = self._list.copy()
            while pos != rear:
                yield currList[pos]
                pos = (pos + 1) % cap
            yield currList[pos]

    def __reversed__(self):
        """Generator yielding the cached contents of the current state of
        the CircularArray in reversed order.
        """
        if self._count > 0:
            cap = self._capacity
            front = self._front
            pos = self._rear
            currList = self._list.copy()
            while pos != front:
                yield currList[pos]
                pos = (pos - 1) % cap
            yield currList[pos]

    def __repr__(self):
        return f'{self.__class__.__name__}(' + ', '.join(map(repr, self)) + ')'

    def __str__(self):
        return "(|" + ", ".join(map(repr, self)) + "|)"

    def __bool__(self):
        """Returns true if circular array is not empty"""
        return self._count > 0

    def __len__(self):
        """Returns current number of values in the circlular array"""
        return self._count

    def __getitem__(self, index: int) -> Any:
        """Get value at a valid index, otherwise raise IndexError"""
        cnt = self._count
        if 0 <= index < cnt:
            return self._list[(self._front + index) % self._capacity]
        elif -cnt <= index < 0:
            return self._list[(self._front + cnt + index) % self._capacity]
        else:
            low = -cnt
            high = cnt - 1
            msg = f'Out of bounds: index = {index} not between {low} and {high}'
            msg += 'while getting value.'
            msg0 = 'Trying to get value from an empty data structure.'
            if cnt > 0:
                raise IndexError(msg)
            else:
                raise IndexError(msg0)

    def __setitem__(self, index: int, value: Any) -> Any:
        """Set value at a valid index, otherwise raise IndexError"""
        cnt = self._count
        if 0 <= index < cnt:
            self._list[(self._front + index) % self._capacity] = value
        elif -cnt <= index < 0:
            self._list[(self._front + cnt + index) % self._capacity] = value
        else:
            low = -cnt
            high = cnt - 1
            msg = f'Out of bounds: index = {index} not between {low} and {high}'
            msg += 'while setting value.'
            msg0 = 'Trying to get value from an empty data structure.'
            if cnt > 0:
                raise IndexError(msg)
            else:
                raise IndexError(msg0)

    def __eq__(self, other):
        """Returns True if all the data stored in both compare as equal.
        Worst case is O(n) behavior for the true case.
        """
        if not isinstance(other, type(self)):
            return False

        if self._count != other._count:
            return False

        left, frontL, capL, cnt = self, self._front, self._capacity, self._count
        right, frontR, capR = other, other._front, other._capacity

        nn = 0
        while nn < cnt:
            if left._list[(frontL+nn)%capL] != right._list[(frontR+nn)%capR]:
                return False
            nn += 1
        return True

    def _double(self) -> None:
        """Double capacity of circular array"""
        if self._front > self._rear:
            data  = self._list[self._front:]
            data += self._list[:self._rear+1]
            data += [None]*(self._capacity)
        else:
            data  = self._list
            data += [None]*(self._capacity)

        self._list, self._capacity,     self._front, self._rear = \
        data,       2 * self._capacity, 0,           self._count - 1

    def compact(self) -> None:
        """Compact the datastructure as much as possible"""
        match self._count:
            case 0:
                self._list, self._capacity, self._front, self._rear = [None]*2, 2, 0, 1
            case 1:
                data = [self._list[self._front], None]
                self._list, self._capacity, self._front, self._rear = data, 2, 0, 0
            case _:
                if self._front > self._rear:
                    data  = self._list[self._front:]
                    data += self._list[:self._rear+1]
                else:
                    data  = self._list[self._front:self._rear+1]
                self._list, self._capacity, self._front, self._rear = data, self._count, 0, self._capacity - 1

    def copy(self) -> CircularArray:
        return CircularArray(*self)

    def reverse(self) -> CircularArray:
        return CircularArray(*reversed(self))

    def pushR(self, d: Any) -> None:
        """Push data on rear of circle"""
        if self._count == self._capacity:
            self._double()
        self._rear = (self._rear + 1) % self._capacity
        self._list[self._rear] = d
        self._count += 1

    def pushL(self, d: Any) -> None:
        """Push data on front of circle"""
        if self._count == self._capacity:
            self._double()
        self._front = (self._front - 1) % self._capacity
        self._list[self._front] = d
        self._count += 1

    def popR(self) -> Any:
        """Pop data off rear of circle array, returns None if empty"""
        if self._count == 0:
            return None
        else:
            d = self._list[self._rear]

            self._count, self._list[self._rear], self._rear = \
                self._count-1, None, (self._rear - 1) % self._capacity

            return d

    def popL(self) -> Any:
        """Pop data off front of circle array, returns None if empty"""
        if self._count == 0:
            return None
        else:
            d = self._list[self._front]

            self._count, self._list[self._front], self._front = \
                self._count-1, None, (self._front+1) % self._capacity

            return d

    def map(self, f: Callable[[Any], Any]) -> CircularArray:
        """Apply function over the circular array's contents and return new
        circular array.
        """
        return CircularArray(*map(f, self))

    def mapSelf(self, f: Callable[[Any], Any]) -> None:
        """Apply function over the circular array's contents mutatng the
        circular array, don't return anything.
        """
        ca  = CircularArray(*map(f, self))
        self._count, self._capacity, self._front, self._rear, self._list = \
            ca._count, ca._capacity, ca._front, ca._rear, ca._list

    # House keeping methods

    def empty(self) -> None:
        """Empty circular array, keep current capacity"""
        self._list, self._front, self._rear = \
            [None]*self._capacity, 0, self._capacity-1

    def capacity(self) -> int:
        """Returns current capacity of circle array"""
        return self._capacity

    def fractionFilled(self) -> float:
        """Returns current capacity of circle array"""
        return self._count/self._capacity

    def resize(self, addCapacity = 0) -> None:
        """Compact circle array and add extra capacity"""
        self.compact()
        if addCapacity > 0:
            self._list = self._list + [None]*addCapacity
            self._capacity += addCapacity
            if self._count == 0:
                self._rear = self._capacity - 1

if __name__ == "__main__":
    pass
