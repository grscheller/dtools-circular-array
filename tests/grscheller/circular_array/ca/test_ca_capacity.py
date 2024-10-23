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
from grscheller.circular_array.ca import ca, CA

class TestCapacity:

    def test_capacity_original(self) -> None:
        ca0: ca[int] = ca()
        assert ca0.capacity() == 2

        ca0 = CA(1, 2)
        assert ca0.fractionFilled() == 2/4

        ca0.pushL(0)
        assert ca0.fractionFilled() == 3/4

        ca0.pushR(3)
        assert ca0.fractionFilled() == 4/4

        ca0.pushR(4)
        assert ca0.fractionFilled() == 5/8

        ca0.pushL(5)
        assert ca0.fractionFilled() == 6/8

        assert len(ca0) == 6
        assert ca0.capacity() == 8

        ca0.resize()
        assert ca0.fractionFilled() == 6/8

        ca0.resize(30)
        assert ca0.fractionFilled() == 6/30

        ca0.resize(3)
        assert ca0.fractionFilled() == 6/8

        ca0.popLD(0)
        ca0.popRD(0)
        ca0.popLD(0)
        ca0.popRD(0)
        assert ca0.fractionFilled() == 2/8
        ca0.resize(3)
        assert ca0.fractionFilled() == 2/4
        ca0.resize(7)
        assert ca0.fractionFilled() == 2/7

    def test_empty(self) -> None:
        c: ca[int] = ca()
        assert c == ca()
        assert c.capacity() == 2
        c.pushL(1, 2, 3, 4, 5)
        assert c.capacity() == 8
        assert c.popLT(2) == (5, 4)
        c.resize()
        assert c.capacity() == 5
        c.resize(11)
        assert c.capacity() == 11
        assert len(c) == 3
        c.pushL(*range(8))
        assert c.capacity() == 11
        c.pushR(*range(2))
        assert c.capacity() == 22

    def test_one(self) -> None:
        c = CA(42)
        assert c.capacity() == 3
        c.resize()
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
