# Copyright 2023-2025 Geoffrey R. Scheller
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

class Test_repr:
    def test_repr(self) -> None:
        ca0: ca[int] = ca()
        assert repr(ca0) == 'CA()'
        foo: ca[int] = eval('CA()')
        bar: ca[int] = eval(repr(ca0))
        assert foo == bar

        ca1: ca[str|int] = ca()
        assert repr(ca1) == 'CA()'
        ca2: ca[int|str] = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        ca1.pushR(1)
        ca1.pushL('foo')
        assert repr(ca1) == "CA('foo', 1)"
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        assert ca1.popLD('bar') == 'foo'
        ca1.pushR(2)
        ca1.pushR(3)
        ca1.pushR(4)
        ca1.pushR(5)
        assert ca1.popL() == 1
        ca1.pushL(42)
        ca1.popR()
        assert repr(ca1) == 'CA(42, 2, 3, 4)'
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        ca3: ca[int] = CA(1, 10, 0, 42)
        ca3.pushR(2, 100, 3)
        assert ca3.popL() == 1
        assert ca3.popR() == 3
        ca3.pushL(9, 8)
        assert ca3.popRT(2) == (100, 2)
        ca3.pushR(1, 2, 3)
        assert repr(ca3) == 'CA(8, 9, 10, 0, 42, 1, 2, 3)'

        ca4: ca[int] = ca([1, 10, 0, 42])
        ca4.pushR(2, 100, 3)
        assert ca4.popL() == 1
        assert ca4.popR() == 3
        ca4.pushL(9, 8)
        assert ca4.popRT(2) == (100, 2)
        ca4.pushR(1, 2, 3)
        assert repr(ca4) == 'CA(8, 9, 10, 0, 42, 1, 2, 3)'
