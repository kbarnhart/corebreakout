# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 0.3 [Unreleased]

### Changed

- Increased flexibility of included scripts
- Converted `docs/*.md` files to `*.rst`

### Added

- Built `sphinx`-generated html docs
- Implemented `CoreColumn.iter_chunks()`
- Added a `CoreColumn` demo notebook
- Added restriction in `setup.py` to require `tensorflow` before install

## 0.2

### Changed

- Modified code format using `black`
- `README.md` installation instructions
- moved paper files to root directory

### Added

- `requirements.txt` (except `imgaug`, which is included in `setup.py`)
- CONTRIBUTING, LICENSE, and CODE_OF_CONDUCT files
- `tests/notebooks`
- tests for `CoreColumn` saving and loading

### Removed

- superfluous notebooks and scripts

## 0.1

Initial private version.
