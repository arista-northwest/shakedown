FROM ubuntu:latest

RUN  \
  apt update && \
  apt install -y build-essential && \
  apt install -y python3 python3-dev && \
  apt install -y python3-pip python3-paramiko && \
  apt install -y python-pip && \
  apt install -y git && \
  apt install -y sshpass

VOLUME ["/shakedown", "/testplan", "/reports"]

COPY init.sh /init.sh

WORKDIR /testplan

ENV PYTHONDONTWRITEBYTECODE 1

# ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/bin/sh", "/init.sh"]
