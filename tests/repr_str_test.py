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

from grscheller.circular_array.ca import CA
from grscheller.fp.nothing import nothing, Nothing

class Test_repr:
    def test_repr(self) -> None:
        ca1: CA[str|int, Nothing] = CA(sentinel=nothing)
        assert repr(ca1) == 'CA(sentinel=nothing)'
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        ca1.pushR(1)
        ca1.pushL('foo')
        assert repr(ca1) == "CA('foo', 1, sentinel=nothing)"
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

        assert ca1.popL() == 'foo'
        ca1.pushR(2)
        ca1.pushR(3)
        ca1.pushR(4)
        ca1.pushR(5)
        assert ca1.popL() == 1
        ca1.pushL(42)
        ca1.popR()
        assert repr(ca1) == 'CA(42, 2, 3, 4, sentinel=nothing)'
        dq2 = eval(repr(ca1))
        assert dq2 == ca1
        assert dq2 is not ca1

        ca3: CA[int, int] = CA(0, 1, 10, 0, 0, 42, 99, sentinel=0, storable=False)
        ca4: CA[int, int] = CA(0, 1, 10, 0, 0, 42, 99, sentinel=0, storable=True)
        assert ca3 != ca4
        ca3.pushR(0, 100, 0)
        assert ca3.popL() == 1
        ca3.pushL(0, 9)
        ca4.pushR(0, 100, 0)
        assert ca4.popL() == 0
        assert ca4.popL() == 1
        ca4.pushL(0, 9)
        assert repr(ca3) == 'CA(9, 10, 42, 99, 100, sentinel=0, storable=False)'
        assert repr(ca4) == 'CA(9, 0, 10, 0, 0, 42, 99, 0, 100, 0, sentinel=0)'
