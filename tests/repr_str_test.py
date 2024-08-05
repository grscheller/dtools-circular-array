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
        ca1: CA[str|int] = CA()
        assert repr(ca1) == 'CA()'
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        ca1.push_rear(1)
        ca1.push_front('foo')
        assert repr(ca1) == "CA('foo', 1)"
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        assert ca1.pop_front_unsafe() == 'foo'
        ca1.push_rear(2)
        ca1.push_rear(3)
        ca1.push_rear(4)
        ca1.push_rear(5)
        assert ca1.pop_front_unsafe() == 1
        ca1.push_front(42)
        ca1.pop_rear_unsafe()
        assert repr(ca1) == 'CA(42, 2, 3, 4)'
        ca2 = eval(repr(ca1))
        assert ca2 == ca1
        assert ca2 is not ca1

        ca3: CA[int] = CA(1, 10, 0, 42, 99)
        ca3.push_rear(2, 100, 3)
        assert ca3.pop_front_unsafe() == 1
        assert ca3.pop_rear_unsafe() == 3
        ca3.push_front(9, 8)
        assert repr(ca3) == 'CA(8, 9, 10, 0, 42, 99, 2, 100)'
