# Copyright 2024 Geoffrey R. Scheller
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

class TestCapacity:

    def test_capacity_original(self) -> None:
        c: CA[int, None] = CA(sentinel=None)
        assert c.capacity() == 2

        c = CA(1, 2, sentinel=None)
        assert c.fractionFilled() == 2/4

        c.pushL(0)
        assert c.fractionFilled() == 3/4

        c.pushR(3)
        assert c.fractionFilled() == 4/4

        c.pushR(4)
        assert c.fractionFilled() == 5/8

        c.pushL(5)
        assert c.fractionFilled() == 6/8

        assert len(c) == 6
        assert c.capacity() == 8

        c.resize()
        assert c.fractionFilled() == 6/8

        c.resize(30)
        assert c.fractionFilled() == 6/30

        c.resize(3)
        assert c.fractionFilled() == 6/8

        c.popL()
        c.popR()
        c.popL()
        c.popR()
        assert c.fractionFilled() == 2/8
        c.resize(3)
        assert c.fractionFilled() == 2/4
        c.resize(7)
        assert c.fractionFilled() == 2/7


    def test_double(self) -> None:
        c: CA[int, int] = CA(1, 2, 3, sentinel=-1)
        assert c.popL() == 1
        assert c.capacity() == 5
        c.double()
        assert c.capacity() == 10
        c.double()
        c.pushL(666)
        c.pushR(0)
        assert len(c) == 4
        assert c.capacity() == 20
        c.resize()
        assert c.capacity() == 6
        c.pushL(2000)
        assert len(c) == 5
        assert c.capacity() == 6
        for ii in range(45):
            if ii % 3 == 0:
                c.pushR(c.popL())
                c.pushL(ii+100)
            else:
                c.pushR(ii+1000)
        assert len(c) == 50
        assert c.capacity() == 96
        jj = len(c)
        assert jj == 50
        while jj > 0:
            kk = c.popL()
            assert kk != -1
            c.pushR(kk)
            jj -= 1
        assert len(c) == 50
        assert c.fractionFilled() == 50/96
        assert c.capacity() == 96
        c.compact()
        assert c.capacity() == 52

    def test_empty(self) -> None:
        c: CA[int, None] = CA(sentinel=None)
        assert c != CA(sentinel=())
        assert c == CA(sentinel=None)
        assert c.capacity() == 2
        c.double()
        assert c.capacity() == 4
        c.compact()
        assert c.capacity() == 2
        c.resize(6)
        assert c.capacity() == 6
        assert len(c) == 0

    def test_one(self) -> None:
        c = CA(42, sentinel=None)
        assert c.capacity() == 3
        c.compact()
        assert c.capacity() == 3
        c.resize(8)
        assert c.capacity() == 8
        assert len(c) == 1
        popped = c.popL()
        assert popped == 42
        assert len(c) == 0
        assert c.capacity() == 8
        assert c.popL() is None
        assert c.popR() is None
        c.pushR(popped)
        assert len(c) == 1
        assert c.capacity() == 8
        c.resize(5)
        assert c.capacity() == 5
        assert len(c) == 1
        c.resize()
        assert c.capacity() == 3
