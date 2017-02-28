# LICENSE CDDL 1.0 + GPL 2.0
#
# Copyright (c) 1982-2016 Oracle and/or its affiliates. All rights reserved.
#
# ORACLE DOCKERFILES PROJECT
# --------------------------
# This is the Dockerfile for Oracle Enterprise Linux for Oracle IDM Images
# 
# REQUIRED FILES TO BUILD THIS IMAGE
# ----------------------------------
#
#
# HOW TO BUILD THIS IMAGE
# -----------------------
# Put all downloaded files in the same directory as this Dockerfile
# Run:
#      $ docker build -t oracle-iam/ol7-iam-base .
#
# Pull base image
# ---------------
FROM oraclelinux:latest

# Maintainer
# ----------
MAINTAINER Paulo Albuquerque <paulogpafilho@gmail.com>

# Environment variables required for this build
# TODO: Remove Proxy Variables before publishing
# -------------------------------------------------------------
ENV MIDDLEWARE_BASE=/u01/oracle \
    CONFIG_BASE=/u02/oracle \
    HTTP_PROXY='http://host:port' \
    HTTPS_PROXY='http://host:port' \
    http_proxy='http://host:port' \
    https_proxy='http://host:port'

# Setup filesystem and oracle user, and file permissions
# ------------------------------------------------------
RUN yum -y install deltarpm && \
    yum -y install unzip binutils compat-libcap1.x86_64 compat-libstdc++-33.x86_64 gcc.x86_64 gcc-c++.x86_64 glibc.x86_64 glibc-devel.x86_64 libaio.x86_64 libaio-devel.x86_64 libgcc.x86_64 libstdc++-4.8.2.x86_64 libstdc++-devel.x86_64 ksh make-3.82 ocfs2-tools-1.2.7 redhat-lsb-core sysstat-10.1.5 && \
    yum clean all && \
    groupadd -g 500 dba && \
    groupadd -g 501 oinstall && \
    useradd -d /home/oracle -g oinstall -G oinstall,dba -m -s /bin/bash oracle && \
    echo oracle:Oracle123 | chpasswd && \
    mkdir -p ${MIDDLEWARE_BASE} ${CONFIG_BASE} && \
    chown -R oracle:oinstall ${MIDDLEWARE_BASE} && \
    chown -R oracle:oinstall ${CONFIG_BASE}

USER oracle
WORKDIR /home/oracle

CMD ["bash"] 
