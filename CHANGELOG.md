# CHANGELOG

PyPI grscheller.circular-array project.

#### Semantic Versioning

* first digit
  * major event, epoch, or paradigm shift
* second digit
  * breaking API changes
  * major changes
* third digit
  * API additions
  * bug fixes
  * minor changes
  * significant documentation updates
* forth digit (development environment only)
  * commit count of "non-trivial" changes/regressions

## Releases and Important Milestones

### Version 3.6.0 - PyPI release date 2024-09-21

* no future changes planned for the foreseeable future
  * feature complete
  * no external dependencies
  * well tested with other grscheller namespace packages
* final API tweaks made
* several more pytest tests added
* made the `compact` method private
  * now called `_compact_storage_capacity`

### Version 3.5.0 - PyPI release date 2024-09-21

* made the `double` method private
  * now called `_double_storage_capacity`
* major docstring improvements
* improved indentation and code alignment
  * now much more Pythonic

### Version 3.4.1 - PyPI release date 2024-08-17

* updated README.md to reflect name changes of CA methods
* docstring improvements

### Version 3.4.0 - PyPI release date 2024-08-15

* updated `__eq__` comparisons
  * first compare elements by identity before equality
    * noticed that is what Python builtins do
    * makes dealing with grscheller.fp.nada module easier
* standardizing docstrings across grscheller PyPI projects

### Version 3.3.0.1 - commit date 2024-08-05

* made a paradigm "regression", preparing for a 3.4.0 release
* felt CA was becoming way too complicated
* grscheller.datastructures needed it to fully embrace type annotations
  * but I was shifting too many features back into grscheller.circular-array
  * want ca to be useful for non-functional applications
* changes made
  * removed grscheller.fp dependency
  * remove _sentinel & _storable slots from CA class
  * remove copy method, just use ca2 = CA(*ca1) to make a shallow copy
  * adjust __repr__ and __str__ methods
  * experimenting with Spinx syntax in docstrings (still using pdoc3)
  * changed nomenclature from "left/right" to "front/rear"
  * unsafe and safe versions of pop & fold functionality
  * left and right folds improvements
    * consolidated `foldL, foldL1, foldR, foldR1` into `foldL` & `foldR`
    * TODO: rename `foldL` to `fold_forward` & `foldR` to `fold_backward`
  * tests working
    * basically I changed pops to unsafe pops and added `try except` blocks
    * safe versions tests needed
      * safe pops return multiple values in tuples
      * will take a `default` value to return
        * if only asked to return 1 value and CA is empty
        * seems to work properly from iPython

### Version 3.2.0 - PyPI release date 2024-07-26

* class name changed CircularArray -> CA
* Now takes a "sentinel" or "fallback" value in its initializer
  * formally used None for this

### Version 3.1.0 - PyPI release date 2024-07-11

* generic typing now being used
* first PyPI release where mult values can be pushed on CircularArray

### Version 3.0.0.0 - commit date 2024-06-28

* CircularArray class now using Generic Type Parameter

* new epoch in development, start of 3.0 series
* now using TypeVars
* API changes
  * foldL(self, f: Callable[[T, T], T]) -> T|None
  * foldR(self, f: Callable[[T, T], T]) -> T|None
  * foldL1(self, f: Callable[[S, T], S], initial: S) -> S
  * foldR1(self, f: Callable[[T, S], S], initial: S) -> S

### Version 2.0.0 - PyPI release date 2024-03-08

* new epoch due to resizing bug fixed on previous commit
  * much improved and cleaned up
  * much better test suite
* method _double() made "public" and renamed double()
* resize(new_size) now resizes to at least new_size

### Version 1.1.0.0 - commit date 2024-03-08

* NEXT PyPI RELEASE WILL BE 2.0.0 !!!!!!!!!!!
* BUGFIX: Fixed a subtle resizing bug
  * bug probably present in all previous versions
    * not previously identified due to inadequate test coverage
  * test coverage improved vastly
* made some major code API changes
  * upon initialization minimizing size of the CircularArray
  * have some ideas on how to to improve API for resizing CircularArrays
  * need to test my other 2 PyPI projects
    * both use circular-array as a dependency

### Version 1.0.1 - PyPI release date 2024-03-01

* docstring updates to match other grscheller PyPI repos

### Version 1.0.0 - PyPI release date 2024-02-10

* first stable release
* dropped minimum Python requirement to 3.10

### Version 0.1.1 - PyPI release date 2024-01-30

* changed circular-array from a package to just a module
  * actually breaking API change
  * version number should have been 0.2.0
* gave CircularArray class foldL & foldR methods

### Version 0.1.0 - PyPI release date 2024-01-28

* initial PyPI grscheller.circular-array release
* migrated Circulararray class from grscheller.datastructutes
* update docstrings to reflect current nomenclature

### Version 0.0.3 - commit date 2024-01-28

* got gh-pages working for the repo

### Version 0.0.2 - commit date 2024-01-28

* pushed repo up to GitHub
* created README.md file for project

### Version 0.0.1 - commit date 2024-01-28

* decided to split Circulararray class out of datastructures
  * will make it its own PyPI project
* got working with datastructures locally
