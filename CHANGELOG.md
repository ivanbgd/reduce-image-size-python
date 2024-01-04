# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 

### Added

- Optional argument for minimum file size for which a user would like to perform file size reduction.
  - It comes in three sizes: S, M, L, for 100 kB, 500 kB and 1 MB, respectively.

### Changed

- When source and destination folders are different, non-supported files will simply be copied to the destination.
  - Previously, they would be left out.

## [0.1.0] - 2023-12-29
This is the very first (initial) fully-functioning version of the program.

### Added

- **JPEG** support.
- **PNG** support.
- "README.md".
- "LICENSE" ("MIT").
- "CHANGELOG.md".
