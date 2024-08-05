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

from __future__ import annotations

from typing import Optional
from grscheller.circular_array.ca import CA
from grscheller.fp.nothing import nothing, Nothing

class TestCircularArray:
    def test_mutate_returns_none(self) -> None:
        ca1: CA[int] = CA()
        assert ca1.push_front(1) == None  # type: ignore # testing for no return
        ca1.push_front(0)
        ca1.push_rear(2)
        ca1.push_rear(3)
        assert ca1.pop_front_unsafe() == 0
        ca1.push_rear(4)
        ca2 = ca1.map(lambda x: x+1)
        assert ca1 is not ca2
        assert ca1 != ca2
        assert len(ca1) == len(ca2)
        assert ca1.pop_front_unsafe() == 1
        while ca1:
            assert ca1.pop_front_unsafe() == ca2.pop_front_unsafe()
        assert len(ca1) == 0
        assert len(ca2) == 1
        assert ca2.pop_rear_unsafe() == 5
        try:
            assert ca2.pop_rear_unsafe()
        except ValueError as ve:
            assert True
            assert str(ve) == 'Method pop_rear_unsafe called on an empty CA'
        else:
            assert False

    def test_push_then_pop(self) -> None:
        c: CA[str] = CA()
        pushed1 = '42'
        c.push_front(pushed1)
        popped1 = c.pop_front_unsafe()
        assert pushed1 == popped1
        assert len(c) == 0
        try:
            c.pop_front_unsafe()
        except ValueError as ve:
            assert str(ve) == 'Method pop_front_unsafe called on an empty CA'
        else:
            assert False
        pushed1 = '0'
        c.push_front(pushed1)
        popped1 = c.pop_rear_unsafe()
        assert pushed1 == popped1 == '0'
        assert not c
        pushed1 = '0'
        c.push_rear(pushed1)
        popped1 = c.pop_front_unsafe()
        assert popped1 is not None
        assert pushed1 == popped1
        assert len(c) == 0
        pushed2 = ''
        c.push_rear(pushed2)
        popped2 = c.pop_rear_unsafe()
        assert pushed2 == popped2
        assert len(c) == 0
        c.push_rear('first')
        c.push_rear('second')
        c.push_rear('last')
        assert c.pop_front_unsafe() == 'first'
        assert c.pop_rear_unsafe() == 'last'
        assert c
        c.pop_front_unsafe()
        assert len(c) == 0

    def test_iterators(self) -> None:
        data: list[int] = [*range(100)]
        c: CA[int] = CA(*data)
        ii = 0
        for item in c:
            assert data[ii] == item
            ii += 1
        assert ii == 100

        data.append(100)
        c = CA(*data)
        data.reverse()
        ii = 0
        for item in reversed(c):
            assert data[ii] == item
            ii += 1
        assert ii == 101

        c0: CA[object] = CA()
        for _ in c0:
            assert False
        for _ in reversed(c0):
            assert False

        data2: list[str] = []
        c0 = CA(*data2, )
        for _ in c0:
            assert False
        for _ in reversed(c0):
            assert False

    def test_equality(self) -> None:
        c1: CA[object] = CA(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        c2: CA[object] = CA(2, 3, 'Forty-Two')
        c2.push_front(1)
        c2.push_rear((7, 11, 'foobar'))
        assert c1 == c2

        tup2 = c2.pop_rear_unsafe()
        assert c1 != c2

        c2.push_rear((42, 'foofoo'))
        assert c1 != c2

        c1.pop_rear_unsafe()
        c1.push_rear((42, 'foofoo'))
        c1.push_rear(tup2)
        c2.push_rear(tup2)
        assert c1 == c2

        holdA = c1.pop_front_unsafe()
        c1.resize(42)
        holdB = c1.pop_front_unsafe()
        holdC = c1.pop_rear_unsafe()
        c1.push_front(holdB)
        c1.push_rear(holdC)
        c1.push_front(holdA)
        c1.push_front(200)
        c2.push_front(200)
        assert c1 == c2

    def test_map(self) -> None:
        c0: CA[int] = CA(1,2,3,10)
        c1 = CA(*c0)
        c2 = c1.map(lambda x: str(x*x - 1))
        assert c2 == CA('0', '3', '8', '99')
        assert c1 != c2
        assert c1 == c0
        assert c1 is not c0
        assert len(c1) == len(c2) == 4

    def test_get_set_items(self) -> None:
        c1 = CA('a', 'b', 'c', 'd')
        c2 = CA(*c1)
        assert c1 == c2
        c1[2] = 'cat'
        c1[-1] = 'dog'
        assert c2.pop_rear_unsafe() == 'd'
        assert c2.pop_rear_unsafe() == 'c'
        c2.push_rear('cat')
        try:
            c2[3] = 'dog'       # no such index
        except IndexError:
            assert True
        else:
            assert False
        assert c1 != c2
        c2.push_rear('dog')
        assert c1 == c2
        c2[1] = 'bob'
        assert c1 != c2
        assert c1.pop_front_unsafe() == 'a'
        c1[0] = c2[1]
        assert c1 != c2
        assert c2.pop_front_unsafe() == 'a'
        assert c1 == c2

    def test_foldL(self) -> None:
        c1: CA[int] = CA()
        try:
            c1.foldL(lambda x, y: x + y)
        except ValueError:
            assert True
        else:
            assert False
        assert c1.foldL(lambda x, y: x + y, initial=42) == 42
        assert c1.foldL(lambda x, y: x + y, initial=0) == 0

        c3: CA[int] = CA(*range(1, 11))
        assert c3.foldL(lambda x, y: x + y) == 55
        assert c3.foldL(lambda x, y: x + y, initial=10) == 65

        c4: CA[int] = CA(*(0,1,2,3,4))

        def f(vs: list[int], v: int) -> list[int]:
            vs.append(v)
            return vs

        empty: list[int] = []
        assert c4.foldL(f, empty) == [0, 1, 2, 3, 4]

    def test_foldR(self) -> None:
        c1: CA[int] = CA()
        try:
            c1.foldR(lambda x, y: x * y)
        except ValueError:
            assert True
        else:
            assert False
        assert c1.foldR(lambda x, y: x * y, initial=42) == 42

        c2: CA[int] = CA(*range(1, 6))
        assert c2.foldR(lambda x, y: x * y) == 120
        assert c2.foldR(lambda x, y: x * y, initial=10) == 1200

        def f(v: int, vs: list[int]) -> list[int]:
            vs.append(v)
            return vs

        c3: CA[int] = CA(*range(5))
        empty: list[int] = []
        assert c3 == CA(0, 1, 2, 3, 4)
        assert c3.foldR(f, empty) == [4, 3, 2, 1, 0]
