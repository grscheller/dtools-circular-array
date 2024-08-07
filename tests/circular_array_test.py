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
        assert ca1.pushL(1) == None  # type: ignore # testing for no return
        ca1.pushL(0)
        ca1.pushR(2)
        ca1.pushR(3)
        assert ca1.popLD(-1) == 0
        ca1.pushR(4)
        ca2 = ca1.map(lambda x: x+1)
        assert ca1 is not ca2
        assert ca1 != ca2
        assert len(ca1) == len(ca2)
        assert ca1.popLD(-1) == 1
        while ca1:
            assert ca1.popLD(-1) == ca2.popLD(-2)
        assert len(ca1) == 0
        assert len(ca2) == 1
        assert ca2.popR() == 5
        try:
            assert ca2.popR()
        except ValueError as ve:
            assert True
            assert str(ve) == 'Method popR called on an empty CA'
        else:
            assert False

    def test_push_then_pop(self) -> None:
        ca: CA[str] = CA()
        pushed1 = '42'
        ca.pushL(pushed1)
        popped1 = ca.popL()
        assert pushed1 == popped1
        assert len(ca) == 0
        try:
            ca.popL()
        except ValueError as ve:
            assert str(ve) == 'Method popL called on an empty CA'
        else:
            assert False
        pushed1 = '0'
        ca.pushL(pushed1)
        popped1 = ca.popR()
        assert pushed1 == popped1 == '0'
        assert not ca
        pushed1 = '0'
        ca.pushR(pushed1)
        popped1 = ca.popLD('666')
        assert popped1 != '666'
        assert pushed1 == popped1
        assert len(ca) == 0
        pushed2 = ''
        ca.pushR(pushed2)
        popped2 = ca.popRD('42')
        assert popped2 != '42'
        assert pushed2 == popped2
        assert len(ca) == 0
        ca.pushR('first')
        ca.pushR('second')
        ca.pushR('last')
        assert ca.popLD('error') == 'first'
        assert ca.popRD('error') == 'last'
        assert ca
        assert len(ca) == 1
        ca.popL()
        assert len(ca) == 0

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
        assert c1.popLD('error') == 'a'
        c1[0] = c2[1]
        assert c1 != c2
        assert c2.popLD('error') == 'a'
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

    def test_pop_tuples(self) -> None:
        ca1 = CA(*range(100))
        zero, one, two, *rest = ca1.popLT(10)
        assert zero == 0
        assert one == 1
        assert two == 2
        assert rest == [3, 4, 5, 6, 7, 8, 9]
        assert len(ca1) == 90

        last, next_to_last, *rest = ca1.popRT(5)
        assert last == 99
        assert next_to_last == 98
        assert rest == [97, 96, 95]
        assert len(ca1) == 85

        ca2 = CA(*ca1)
        assert len(ca1.popRT(0)) == 0
        assert ca1 == ca2

    def test_fold(self) -> None:
        ca1 = CA(*range(1, 101))
        assert ca1.foldL(lambda acc, d: acc + d) == 5050
        assert ca1.foldR(lambda d, acc: d + acc) == 5050

        def fl(acc: int, d: int) -> int:
            return acc*acc - d

        def fr(d: int, acc: int) -> int:
            return acc*acc - d

        ca2 = CA(2, 3, 4)
        assert ca2.foldL(fl) == -3
        assert ca2.foldR(fr) == 167

    def test_readme(self) -> None:
        ca = CA(1, 2, 3)
        assert ca.popL() == 1
        assert ca.popR() == 3
        ca.pushR(42, 0)
        ca.pushL(0, 1)
        assert repr(ca) == 'CA(1, 0, 2, 42, 0)'
        assert str(ca) == '(|1, 0, 2, 42, 0|)'

        ca = CA(*range(1,11))
        assert repr(ca) == 'CA(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)'
        assert str(ca) == '(|1, 2, 3, 4, 5, 6, 7, 8, 9, 10|)'
        assert len(ca) == 10
        tup3 = ca.popLT(3)
        tup4 = ca.popRT(4)
        assert tup3 == (1, 2, 3)
        assert tup4 == (10, 9, 8, 7)

        assert ca == CA(4, 5, 6)
        four, *rest = ca.popLT(1000)
        assert four == 4
        assert rest == [5, 6]
        assert len(ca) == 0

        ca = CA(1, 2, 3)
        assert ca.popLD(42) == 1
        assert ca.popRD(42) == 3
        assert ca.popLD(42) == 2
        assert ca.popRD(42) == 42
        assert ca.popLD(42) == 42
        assert len(ca) == 0
