# Change Log

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