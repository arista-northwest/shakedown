FROM ubuntu:latest

RUN  \
  apt update && \
  apt install -y build-essential \
    python3 \
    python3-dev \
    python-is-python3 \
    python3-pip \
    python3-paramiko \
    git \
    sshpass

VOLUME ["/shakedown", "/testplan", "/reports"]

COPY init.sh /init.sh

WORKDIR /testplan

ENV PYTHONDONTWRITEBYTECODE 1

# ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/bin/sh", "/init.sh"]
