# CHANGELOG

PyPI grscheller.circular-array PyPI project.

## Semantic Versioning

* first digit:
  * major event, epoch, or paradigm shift
* second digit:
  * breaking API changes
  * major changes
* third digit:
  * API additions
  * bug fixes
  * minor changes
  * significant documentation updates
* forth digit:
  * development only

## Releases and Important Milestones

### Version 3.1.0 - PyPI release date 2024-07-11

* generic typing now being used
* first PyPI release where mult values can be pushed on CircularArray

### Version 3.0.3.0 - commit date 2024-07-04

* can now directly push multiple values onto a CircularArray

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
    * not previously identified due to inadequate test coverage!
  * improved test coverage vastly
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
* migrated Circulararray class from grscheller.datastrucutes
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
