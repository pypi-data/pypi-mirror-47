# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

- n/a

## [0.2.1] - 2019-06-17

### Fixed
- Fixed various compatibility issues with old versions of libraries

## [0.2.0] - 2019-06-14

### Added
- Task error_summary and error_details are now initialized appropriately
  with data from Pulp
- Client now logs Pulp load every few minutes when awaiting tasks
- Client now logs warnings when Pulp operations are being retried
- Cancelling a future now attempts to cancel underlying Pulp task(s)
- Deleting a resource which is already nonexistent now succeeds

## [0.1.1] - 2019-06-13

### Fixed
- Fixed missing schema files from distribution

## 0.1.0 - 2019-06-13

- Initial release to PyPI

[Unreleased]: https://github.com/release-engineering/pubtools-pulplib/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/release-engineering/pubtools-pulplib/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/release-engineering/pubtools-pulplib/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/release-engineering/pubtools-pulplib/compare/v0.1.0...v0.1.1
