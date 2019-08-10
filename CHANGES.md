# Change Log

## Version 1.2: Fall 2019 releasee

* Added `assert_error` to `testcase` for checking function asserts
* Added code rewriting to `modlib` (still unexposed) to guard against infinite loops
* Modified `Environment` in `modlib` to load from file or source string
* Added feature to `Environment` to execute code as as a script (`__name__ == '__main__'`)

## Version 1.1.1: Grading Support

* Added experimental `modlib` module (unexposed)
* Reverted to wheel over egg

## Version 1.1: eCornell Release

* `testcase` functions now support custom error messages
* `geom` package refactored to minimize `numpy` (to prevent memory crash in Python Tutor)

## Version 1.0.5: Second URL Tool Fix

* Added unverified context to fix problem with `SSLContext`

## Version 1.0.4: URL Tool Fix

* Added `SSLContext` support to connect to https://
* Fixed another race condition in `turtle` package

## Version 1.0.3: Turtle Fix

* Another attempt to fix race condition in `turtle` package

## Version 1.0.2: Pre-Semester Fixes

* Fixed problem in web color parsing
* Fixed race condition in `turtle` package

## Version 1.0: Official Release

* `filetools` officially added to release
* `filetools` adapted to use official `csv` package
* `numpy` imports moved inside methods (to prevent memory crash in Python Tutor)

## Version 0.6: Proof of Concept

The following packages were available on release.

* `geom`
* `turtle`
* `colors`
* `strings`
* `testcase`
* `tuples`
* `urltools`

Package `filetools` was included, but not publicly exposed.