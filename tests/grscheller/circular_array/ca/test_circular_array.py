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
from grscheller.circular_array.ca import ca, CA

class TestCircularArray:
    def test_mutate_returns_none(self) -> None:
        ca1: ca[int] = ca()
        assert ca1.pushL(1) == None  # type: ignore # this is test!
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
            assert str(ve) == 'Method popR called on an empty ca'
        else:
            assert False

    def test_push_then_pop(self) -> None:
        ca0: ca[str] = ca()
        pushed1 = '42'
        ca0.pushL(pushed1)
        popped1 = ca0.popL()
        assert pushed1 == popped1
        assert len(ca0) == 0
        try:
            ca0.popL()
        except ValueError as ve:
            assert str(ve) == 'Method popL called on an empty ca'
        else:
            assert False
        pushed1 = '0'
        ca0.pushL(pushed1)
        popped1 = ca0.popR()
        assert pushed1 == popped1 == '0'
        assert not ca0
        pushed1 = '0'
        ca0.pushR(pushed1)
        popped1 = ca0.popLD('666')
        assert popped1 != '666'
        assert pushed1 == popped1
        assert len(ca0) == 0
        pushed2 = ''
        ca0.pushR(pushed2)
        popped2 = ca0.popRD('42')
        assert popped2 != '42'
        assert pushed2 == popped2
        assert len(ca0) == 0
        ca0.pushR('first')
        ca0.pushR('second')
        ca0.pushR('last')
        assert ca0.popLD('error') == 'first'
        assert ca0.popRD('error') == 'last'
        assert ca0
        assert len(ca0) == 1
        ca0.popL()
        assert len(ca0) == 0

    def test_iterators(self) -> None:
        data: list[int] = [*range(100)]
        c: ca[int] = ca(data)
        ii = 0
        for item in c:
            assert data[ii] == item
            ii += 1
        assert ii == 100

        data.append(100)
        c = ca(data)
        data.reverse()
        ii = 0
        for item in reversed(c):
            assert data[ii] == item
            ii += 1
        assert ii == 101

        c0: ca[object] = ca()
        for _ in c0:
            assert False
        for _ in reversed(c0):
            assert False

        data2: list[str] = []
        c0 = ca(data2, )
        for _ in c0:
            assert False
        for _ in reversed(c0):
            assert False

    def test_equality(self) -> None:
        c1: ca[object] = CA(1, 2, 3, 'Forty-Two', (7, 11, 'foobar'))
        c2: ca[object] = CA(2, 3, 'Forty-Two')
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
        c0: ca[int] = CA(1,2,3,10)
        c1 = ca(c0)
        c2 = c1.map(lambda x: str(x*x - 1))
        assert c2 == CA('0', '3', '8', '99')
        assert c1 != c2
        assert c1 == c0
        assert c1 is not c0
        assert len(c1) == len(c2) == 4

    def test_get_set_items(self) -> None:
        c1 = CA('a', 'b', 'c', 'd')
        c2 = ca(c1)
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
        c1: ca[int] = ca()
        try:
            c1.foldL(lambda x, y: x + y)
        except ValueError:
            assert True
        else:
            assert False
        assert c1.foldL(lambda x, y: x + y, initial=42) == 42
        assert c1.foldL(lambda x, y: x + y, initial=0) == 0

        c3: ca[int] = ca(range(1, 11))
        assert c3.foldL(lambda x, y: x + y) == 55
        assert c3.foldL(lambda x, y: x + y, initial=10) == 65

        c4: ca[int] = ca((0,1,2,3,4))

        def f(vs: list[int], v: int) -> list[int]:
            vs.append(v)
            return vs

        empty: list[int] = []
        assert c4.foldL(f, empty) == [0, 1, 2, 3, 4]

    def test_foldR(self) -> None:
        c1: ca[int] = ca()
        try:
            c1.foldR(lambda x, y: x * y)
        except ValueError:
            assert True
        else:
            assert False
        assert c1.foldR(lambda x, y: x * y, initial=42) == 42

        c2: ca[int] = ca(range(1, 6))
        assert c2.foldR(lambda x, y: x * y) == 120
        assert c2.foldR(lambda x, y: x * y, initial=10) == 1200

        def f(v: int, vs: list[int]) -> list[int]:
            vs.append(v)
            return vs

        c3: ca[int] = ca(range(5))
        empty: list[int] = []
        assert c3 == CA(0, 1, 2, 3, 4)
        assert c3.foldR(f, empty) == [4, 3, 2, 1, 0]

    def test_pop_tuples(self) -> None:
        ca1 = ca(range(100))
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

        ca2 = ca(ca1)
        assert len(ca1.popRT(0)) == 0
        assert ca1 == ca2

    def test_fold(self) -> None:
        ca1 = ca(range(1, 101))
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
        ca0 = CA(1, 2, 3)
        assert ca0.popL() == 1
        assert ca0.popR() == 3
        ca0.pushR(42, 0)
        ca0.pushL(0, 1)
        assert repr(ca0) == 'CA(1, 0, 2, 42, 0)'
        assert str(ca0) == '(|1, 0, 2, 42, 0|)'

        ca0 = ca(range(1,11))
        assert repr(ca0) == 'CA(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)'
        assert str(ca0) == '(|1, 2, 3, 4, 5, 6, 7, 8, 9, 10|)'
        assert len(ca0) == 10
        tup3 = ca0.popLT(3)
        tup4 = ca0.popRT(4)
        assert tup3 == (1, 2, 3)
        assert tup4 == (10, 9, 8, 7)

        assert ca0 == CA(4, 5, 6)
        four, *rest = ca0.popLT(1000)
        assert four == 4
        assert rest == [5, 6]
        assert len(ca0) == 0

    def test_pop(self) -> None:

        ca1 = CA(1, 2, 3)
        assert ca1.popLD(42) == 1
        assert ca1.popRD(42) == 3
        assert ca1.popLD(42) == 2
        assert ca1.popRD(42) == 42
        assert ca1.popLD(42) == 42
        assert len(ca1) == 0

        ca2: ca[int] = CA(0,1,2,3,4,5,6)
        assert ca2.popL() == 0
        assert ca2.popR() == 6
        assert ca2 == CA(1,2,3,4,5)
        ca2.pushL(0)
        ca2.pushR(6)
        assert ca2 == CA(0,1,2,3,4,5,6)
        ca2.pushL(10,11,12)
        assert ca2 == CA(12,11,10,0,1,2,3,4,5,6)
        ca2.pushR(86, 99)
        assert ca2 == CA(12,11,10,0,1,2,3,4,5,6,86,99)
        control = ca2.popRT(2)
        assert control == (99, 86)
        assert ca2 == CA(12,11,10,0,1,2,3,4,5,6)

        ca3: ca[int] = ca(range(1, 10001))
        ca3_L_first100 = ca3.popLT(100)
        ca3_R_last100 = ca3.popRT(100)
        ca3_L_prev10 = ca3.popLT(10)
        ca3_R_prev10 = ca3.popRT(10)
        assert ca3_L_first100 == tuple(range(1, 101))
        assert ca3_R_last100 == tuple(range(10000, 9900, -1))
        assert ca3_L_prev10 == tuple(range(101, 111))
        assert ca3_R_prev10 == tuple(range(9900, 9890, -1))

        ca4: ca[int] = ca(range(1, 10001))
        ca4_L_first100 = ca4.popLT(100)
        ca4_L_next100 = ca4.popLT(100)
        ca4_L_first10 = ca4.popLT(10)
        ca4_L_next10 = ca4.popLT(10)
        assert ca4_L_first100 == tuple(range(1, 101))
        assert ca4_L_next100 == tuple(range(101, 201))
        assert ca4_L_first10 == tuple(range(201, 211))
        assert ca4_L_next10 == tuple(range(211, 221))

        # Below seems to show CPython tuples are evaluated left to right
        ca5: ca[int] = ca(range(1, 10001))
        ca5_L_first100, ca5_L_next100, ca5_L_first10, ca5_L_next10 = \
          ca5.popLT(100), ca5.popLT(100), ca5.popLT(10), ca5.popLT(10)
        assert ca5_L_first100 == tuple(range(1, 101))
        assert ca5_L_next100 == tuple(range(101, 201))
        assert ca5_L_first10 == tuple(range(201, 211))
        assert ca5_L_next10 == tuple(range(211, 221))

    def test_state_caching(self) -> None:
        expected = CA((0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                      (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 1),
                      (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 1),
                      (3, 0), (3, 1), (3, 2), (3, 3), (3, 4), (3, 1), (3, 3),
                      (4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 1), (4, 3))
        foo = CA(0, 1, 2, 3, 4)
        bar = ca[tuple[int, int]]()

        for ii in foo:
            if ii % 2 == 1:
                foo.pushR(ii)
            for jj in foo:
                bar.pushR((ii, jj))

        assert  bar == expected  # if foo were a list, outer loop above never returns
