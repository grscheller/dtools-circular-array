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
        ca1: CA[int, None] = CA(s=None)
        assert ca1.pushL(1) == None  # type: ignore # testing for no return
        ca1.pushL(0)
        ca1.pushR(2)
        ca1.pushR(3)
        assert ca1.popL() == 0
        ca1.pushR(4)
        ca2 = ca1.map(lambda x: x+1)
        assert ca1 is not ca2
        assert ca1 != ca2
        assert len(ca1) == len(ca2)
        assert ca1.popL() == 1
        while ca1:
            assert ca1.popL() == ca2.popL()
        assert len(ca1) == 0
        assert len(ca2) == 1
        assert ca2.popR() == 5
        assert ca2.popL() is None

    def test_push_then_pop(self) -> None:
        c: CA[str, None] = CA(s=None)
        pushed1 = '42'
        c.pushL(pushed1)
        popped1 = c.popL()
        assert pushed1 == popped1
        assert len(c) == 0
        assert c.popL() is None
        pushed1 = '0'
        c.pushL(pushed1)
        popped1 = c.popR()
        assert pushed1 == popped1 == '0'
        assert not c
        pushed1 = '0'
        c.pushR(pushed1)
        popped1 = c.popL()
        assert popped1 is not None
        assert pushed1 == popped1
        assert len(c) == 0
        pushed2 = ''
        c.pushR(pushed2)
        popped2 = c.popR()
        assert pushed2 == popped2
        assert len(c) == 0
        c.pushR('first')
        c.pushR('second')
        c.pushR('last')
        assert c.popL() == 'first'
        assert c.popR() == 'last'
        assert c
        c.popL()
        assert len(c) == 0

    def test_iterators(self) -> None:
        data: list[int] = [*range(100)]
        c: CA[int, tuple[()]]= CA(*data, s=())
        ii = 0
        for item in c:
            assert data[ii] == item
            ii += 1
        assert ii == 100

        data.append(100)
        c = CA(*data, s=())
        data.reverse()
        ii = 0
        for item in reversed(c):
            assert data[ii] == item
            ii += 1
        assert ii == 101

        c0: CA[object, tuple[()]] = CA(s=())
        for _ in c0:
            assert False
        for _ in reversed(c0):
            assert False

        data2: list[str] = []
        c0 = CA(*data2, s=())
        for _ in c0:
            assert False
        for _ in reversed(c0):
            assert False

    def test_equality(self) -> None:
        c1: CA[object, tuple[()]] = CA(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'), s=())
        c2: CA[object, tuple[()]] = CA(2, 3, 'Forty-Two', s=())
        c2.pushL(1)
        c2.pushR((7, 11, 'foobar'))
        assert c1 == c2

        tup2 = c2.popR()
        assert c1 != c2

        c2.pushR((42, 'foofoo'))
        assert c1 != c2

        c1.popR()
        c1.pushR((42, 'foofoo'))
        c1.pushR(tup2)
        c2.pushR(tup2)
        assert c1 == c2

        holdA = c1.popL()
        c1.resize(42)
        holdB = c1.popL()
        holdC = c1.popR()
        c1.pushL(holdB)
        c1.pushR(holdC)
        c1.pushL(holdA)
        c1.pushL(200)
        c2.pushL(200)
        assert c1 == c2

    def test_map(self) -> None:
        c0: CA[int, None] = CA(1,2,3,10, s=None)
        c1 = c0.copy()
        c2 = c1.map(lambda x: x*x-1)
        assert c2 == CA(0,3,8,99, s=None)
        assert c1 != c2
        assert c1 == c0
        assert c1 is not c0
        assert len(c1) == len(c2) == 4

    def test_get_set_items(self) -> None:
        c1: CA[str, str] = CA('a', 'b', 'c', 'd', s = '')
        c2 = c1.copy()
        assert c1 == c2
        c1[2] = 'cat'
        c1[-1] = 'dog'
        assert c2.popR() == 'd'
        assert c2.popR() == 'c'
        c2.pushR('cat')
        try:
            c2[3] = 'dog'       # no such index
        except IndexError:
            assert True
        else:
            assert False
        assert c1 != c2
        c2.pushR('dog')
        assert c1 == c2
        c2[1] = 'bob'
        assert c1 != c2
        assert c1.popL() == 'a'
        c1[0] = c2[1]
        assert c1 != c2
        assert c2.popL() == 'a'
        assert c1 == c2

    def test_foldL(self) -> None:
        c1: CA[int, None] = CA(s=None)
        assert c1.foldL(lambda x, y: x + y) == None
        assert c1.foldL(lambda x, y: x + y, initial=42) == 42

        c2: CA[int, Nothing] = CA(s=nothing)
        assert c2.foldL(lambda x, y: x + y) == nothing
        assert c2.foldL(lambda x, y: x + y, initial=0) == 0

        c3: CA[int, None] = CA(*range(1, 11), s=None)
        assert c3.foldL(lambda x, y: x + y) == 55
        assert c3.foldL(lambda x, y: x + y, initial=10) == 65

        c4: CA[int, None] = CA(*(0,1,2,3,4), s=None)

        def f(vs: list[int], v: int) -> list[int]:
            vs.append(v)
            return vs

        empty: list[int] = []
        assert c4.foldL(f, empty) == [0, 1, 2, 3, 4]

    def test_foldR(self) -> None:
        c1: CA[int, None] = CA(s=None)
        assert c1.foldR(lambda x, y: x * y) == None
        assert c1.foldR(lambda x, y: x * y, initial=42) == 42

        c2: CA[int, None] = CA(*range(1, 6), s=None)
        assert c2.foldR(lambda x, y: x * y) == 120
        assert c2.foldR(lambda x, y: x * y, initial=10) == 1200

        def f(v: int, vs: list[int]) -> list[int]:
            vs.append(v)
            return vs

        c3: CA[int, tuple[()]] = CA(*range(5), s=())
        empty: list[int] = []
        assert c3 == CA(0, 1, 2, 3, 4, s=())
        assert c3.foldR(f, empty) == [4, 3, 2, 1, 0]
