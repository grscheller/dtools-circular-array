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

from grscheller.circular_array import CircularArray

class TestCapacity:

    def test_capacitya_original(self):
        c = CircularArray()
        assert c.capacity() == 2

        c = CircularArray(1, 2)
        assert c.fractionFilled() == 2/4

        c.pushL(0)
        assert c.fractionFilled() == 3/4

        c.pushR(3)
        assert c.fractionFilled() == 4/4

        c.pushR(4)
        c.pushL(5)
        assert c.fractionFilled() == 6/8

        assert len(c) == 6
        assert c.capacity() == 8

        c.resize()
        assert c.fractionFilled() == 6/6

        c.resize(30)
        assert c.fractionFilled() == 6/36

    def test_double(self):
        c = CircularArray(1, 2, 3)
        assert c.popL() == 1
        assert c.capacity() == 5
        c._double()
        assert c.capacity() == 10
        c._double()
        c.pushL(42)
        c.pushR(0)
        assert len(c) == 4
        assert c.capacity() == 20
        c.resize()
        assert c.capacity() == 4
        c.pushL(1)
        assert len(c) == 5
        assert c.capacity() == 8
        for ii in range(45):
            if ii % 3 == 0:
                c.pushR(c.popL())
                c.pushL(ii)
            else:
                c.pushR(ii)
        assert len(c) == 50
        assert c.capacity() == 64
        jj = len(c)
        while jj > 0:
            kk = c.popL()
            assert kk is not None
            c.pushR(jj)
            jj -= 1
