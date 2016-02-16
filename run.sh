#!/bin/bash
mkdir -p target/website
mkdir -p target/transactions
JAVA_OPTS="-Xdebug -Xrunjdwp:transport=dt_socket,address=8005,server=y,suspend=n"

mvn package && \
java $JAVA_OPTS \
          -Ddylan.store=src/test/resources/ \
          -DPORT=8085 \
          -Drestolino.packageprefix=com.github.davidcarboni.dylan.api \
          -jar target/*-jar-with-dependencies.jar
