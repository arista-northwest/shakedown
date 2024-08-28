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
    sshpass \
    iputils-ping \
    dnsutils \
    nmap \
    vim



RUN \
  pip3 install --break-system-packages --user \
    nest_asyncio \
    tornado \
    jupyter \
    pandas \
    numpy \
    matplotlib \
    pexpect  \
    future \
    pytest \
    jinja2 \
    requests \
    sh \
    mistune \
    tinydb \
    tinymongo \
    eapi-py==0.4.1 \
    tox

VOLUME ["/shakedown", "/testplan", "/reports"]

COPY init.sh /init.sh

WORKDIR /testplan

ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH=/root/.local/bin:$PATH

# ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["/bin/sh", "/init.sh"]
