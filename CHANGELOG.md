# CHANGELOG

Changelog for the grscheller.circular-array PyPI project.
Version numbers for PyPI releases begin with a `v`.

**Semantic Versioning:**

* first digit:
  * major event, epoch, or paradigm shift
* second digit:
  * PyPI breaking API changes or PyPI major changes
* third digit:
  * PyPI API additions, PyPI bugfixes or minor changes
  * PyPI significant documentation updates
  * development API breaking changes
* forth digit (development environment only):
  * development API additions
  * commit count (thrashing)
  * not to be taken too seriously

## Version v2.0.0 - PyPI release date 2024-03-08

* New "epoch" due to resizing bug fixed on previous commit
  * much improved and cleaned up
  * much better test suite
* method _double() made "public" and renamed double() 
* resize(newsize) now resizes to at least newsize

## Version 1.1.0.0 - commit date 2024-03-08

* NEXT PyPI RELEASE WILL BE 2.0.0 !!!!!!!!!!!
* BUGFIX: Fixed a subtle resizing bug
  * bug probably present in all previous versions
    * not previously identified due to inadequate test coverage!
    * debating pulling all previous PyPI releases
  * improved test coverage vastly
* made some major code API changes
  * upon initialization minimizing size of the CircularArray
  * have some ideas on how to to improve API for resizing CircularArrays
  * need to test my other 2 PyPI projects
    * both use circular-array as a dependency

## Version v1.0.1 - PyPI release date 2024-03-01

* docstring updates to match other grscheller PyPI repos

## Version v1.0.0 - PyPI release date 2024-02-10

* first stable release
* dropped minimum Python requirement to 3.10

## Version v0.1.1 - PyPI release date 2024-01-30

* changed circular-array from a package to just a module
  * actually breaking API change
  * version number should have been v0.2.0
* gave CircularArray class foldL & foldR methods

## Version v0.1.0 - PyPI release date 2024-01-28

* initial PyPI grscheller.circular-array release
* migrated Circulararray class from grscheller.datastrucutes
* update docstrings to reflect current nomenclature

## Version 0.0.3 - commit date 2024-01-28

* got gh-pages working for the repo

## Version 0.0.2 - commit date 2024-01-28

* pushed repo up to GitHub
* created README.md file for project

## Version 0.0.1 - commit date 2024-01-28

* decided to split Circulararray class out of datastructures
  * will make it its own PyPI project
* got working with datastructures locally
