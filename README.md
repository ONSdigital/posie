[![Build Status](https://travis-ci.org/ONSdigital/Posie.svg?branch=master)](https://travis-ci.org/ONSdigital/Posie)

![Logo](http://www.80snostalgia.com/files/fluposie.jpg)

# Posie

Posie is a decryption service written in Python. It is a component of the Office of National Statistics (ONS) Survey Data Exchange (SDE) project, which takes an encrypted json payload and transforms it into a number of formats for use within the ONS.

It exposes two endpoints '/key' and '/decrypt' which expose a public key and the decryption service respectively.

The key endpoint exposes a der format public key and the decrypt endpoint decrypts and returns the POST data it is sent.

All requests have a json content type.

## Installation

Using virtualenv and pip, create a new environment and install within using:

	$ pip install -r requirements.txt

It's also possible to install within a container using docker. From the posie directory:

	$ docker build -t posie . 