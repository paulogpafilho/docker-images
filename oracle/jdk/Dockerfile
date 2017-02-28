# LICENSE CDDL 1.0 + GPL 2.0
#
# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
#
FROM oracle-iam/ol7-iam-base

MAINTAINER Paulo Albuquerque <paulogpafilho@gmail.com>

USER root

ENV JAVA_PKG=jdk-7u79-linux-x64.tar.gz \
    JAVA_HOME=${MIDDLEWARE_BASE}/jdk1.7.0_79

ADD $JAVA_PKG ${MIDDLEWARE_BASE}

RUN chown -R oracle:oinstall ${MIDDLEWARE_BASE}

USER oracle

WORKDIR /home/oracle

ENV PATH=$PATH:$JAVA_HOME/bin
