### Unreleased

### 1.9.3 2019-11-08
  - Add python 3.8 to travis builds
  
### 1.9.2 2019-09-26
  - Update werkzeug to 0.15.6 to fix security issue
  - Update all packages to latest version, where possible.

### 1.9.1 2019-08-13
  - Update sdc-cryptography to 0.4.0

### 1.9.0 2019-05-31
  - Remove python 3.4 and 3.5 from travis builds
  - Add python 3.7 to travis builds
  - Update urllib3, Jinja2 and pyyaml to fix security issues

### 1.8.1 2019-01-22
  - Update version of sdc-cryptography to 0.3.0

### 1.8.0 2018-09-11
  - Update dependencies

### 1.7.0 2018-08-15
  - Remove unused packages, updated packages that had security vulnerabilties.
  
### 1.6.0 2018-01-04
  - Add /info healthcheck endpoint

### 1.5.0 2017-11-21
  - Update version of sdc-cryptography to 0.2.1
  - Remove sdx-common git clone in Dockerfile
  - Add config specific to service to config file
  - Change to use pytest to improve test output. Also improve code coverage stats
  - Add Cloudfoundry deployment files
  - Remove sdx-common logging

### 1.4.0 2017-09-11
  - Ensure integrity and version of library dependencies
  - Remove enum34 from requirements.txt
  - Bind logger to tx_id on decrypt
  - Change to use new sdc-cryptography library
  - Upgrade to the latest sdc-crytography library

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
