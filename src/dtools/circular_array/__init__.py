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

"""### Developer Tools - Circular Array Data Structure

Package for an indexable, sliceable, auto-resizing circular array
data structure with amortized O(1) pushes and pops either end.

#### Circular Array Data Structure

##### *module* dtools.circular_array.ca

Circular array data structure.

- *class* dtools.circular_array.ca.CA
  - initializer takes 1 or 0 iterables
- *function* dtools.circular_array.ca.ca
  - factory function taking a variable number of arguments

"""

__version__ = '3.12.0'
__author__ = 'Geoffrey R. Scheller'
__copyright__ = 'Copyright (c) 2023-2025 Geoffrey R. Scheller'
__license__ = 'Apache License 2.0'
