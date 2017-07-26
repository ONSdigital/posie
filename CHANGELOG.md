### Unreleased
  - Remove enum34 from requirements.txt
  - Bind logger to tx_id on decrypt
  - Reworking to use new sdc-cryptography library

### 1.3.0 2017-07-25
  - Change all instances of ADD to COPY in Dockerfile
  - Remove use of SDX_HOME variable in makefile

### 1.2.0 2017-07-10
  - Add environment variables to README
  - Remove secure data from logging messages
  - Correct license attribution
  - Add codacy badge
  - Adding sdx-common functionality
  - Updating logger format using sdx-common
  - Add support for codecov to see unit test coverage
  - Update and pin version of sdx-common to 0.7.0
  - Added additional logging


### 1.1.3 2017-03-15
  - Add version number to log

### 1.1.2 2017-02-16
  - Add change log
  - Update python module _cryptography_: `1.5.3` -> `1.7.1`
  - Update python module _cffi_: `1.5.2` -> `1.9.1`

### 1.1.1 2016-11-16
  - Fix [#33](https://github.com/ONSdigital/sdx-decrypt/issues/33) by update to python module _cryptography_: `1.2.3` -> `1.5.3`

### 1.1.0 2016-10-24
  - Add new `/healthcheck` endpoint

### 1.0.0 2016-08-11
  - Initial release
