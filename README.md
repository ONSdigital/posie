[![Build Status](https://travis-ci.org/ONSdigital/Posie.svg?branch=master)](https://travis-ci.org/ONSdigital/Posie)

![Logo](http://www.80snostalgia.com/files/fluposie.jpg)

# Posie

Posie is a decryption service. It exposes two endpoints '/key' and '/decrypt' which expose a public key and the decryption service respectively.

The key endpoint exposes a der format public key and the decrypt endpoint decrypts and returns the POST data it is sent.

All requests have a json content type..