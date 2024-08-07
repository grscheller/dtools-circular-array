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

from grscheller.circular_array.ca import CA

class TestCapacity:

    def test_capacity_original(self) -> None:
        ca: CA[int] = CA()
        assert ca.capacity() == 2

        ca = CA(1, 2)
        assert ca.fractionFilled() == 2/4

        ca.pushL(0)
        assert ca.fractionFilled() == 3/4

        ca.pushR(3)
        assert ca.fractionFilled() == 4/4

        ca.pushR(4)
        assert ca.fractionFilled() == 5/8

        ca.pushL(5)
        assert ca.fractionFilled() == 6/8

        assert len(ca) == 6
        assert ca.capacity() == 8

        ca.resize()
        assert ca.fractionFilled() == 6/8

        ca.resize(30)
        assert ca.fractionFilled() == 6/30

        ca.resize(3)
        assert ca.fractionFilled() == 6/8

        ca.popLD(0)
        ca.popRD(0)
        ca.popLD(0)
        ca.popRD(0)
        assert ca.fractionFilled() == 2/8
        ca.resize(3)
        assert ca.fractionFilled() == 2/4
        ca.resize(7)
        assert ca.fractionFilled() == 2/7


    def test_double(self) -> None:
        ca: CA[int] = CA(1, 2, 3)
        assert ca.popLD(0) == 1
        assert ca.capacity() == 5
        ca.double()
        assert ca.capacity() == 10
        ca.double()
        ca.pushL(666)
        ca.pushR(0)
        assert len(ca) == 4
        assert ca.capacity() == 20
        ca.resize()
        assert ca.capacity() == 6
        ca.pushL(2000)
        assert len(ca) == 5
        assert ca.capacity() == 6
        for ii in range(45):
            if ii % 3 == 0:
                ca.pushR(ca.popLD(42))
                ca.pushL(ii+100)
            else:
                ca.pushR(ii+1000)
        assert len(ca) == 50
        assert ca.capacity() == 96
        jj = len(ca)
        assert jj == 50
        while jj > 0:
            kk = ca.popL()
            assert kk != -1
            ca.pushR(kk)
            jj -= 1
        assert len(ca) == 50
        assert ca.fractionFilled() == 50/96
        assert ca.capacity() == 96
        ca.compact()
        assert ca.capacity() == 52

    def test_empty(self) -> None:
        c: CA[int] = CA()
        assert c == CA()
        assert c.capacity() == 2
        c.double()
        assert c.capacity() == 4
        c.compact()
        assert c.capacity() == 2
        c.resize(6)
        assert c.capacity() == 6
        assert len(c) == 0

    def test_one(self) -> None:
        c = CA(42)
        assert c.capacity() == 3
        c.compact()
        assert c.capacity() == 3
        c.resize(8)
        assert c.capacity() == 8
        assert len(c) == 1
        popped = c.popLD(0)
        assert popped == 42
        assert len(c) == 0
        assert c.capacity() == 8

        try:
            c.popL()
        except ValueError as ve:
            str(ve) == 'foofoo'
        else:
            assert False

        try:
            c.popR()
        except ValueError as ve:
            str(ve) == 'foofoo'
        else:
            assert False

        c.pushR(popped)
        assert len(c) == 1
        assert c.capacity() == 8
        c.resize(5)
        assert c.capacity() == 5
        assert len(c) == 1
        c.resize()
        assert c.capacity() == 3
