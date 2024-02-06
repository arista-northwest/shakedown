FROM ubuntu:latest

RUN  \
  apt update && \
  apt install -y build-essential libffi-dev && \
  apt install -y git sshpass && \
  apt install -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-paramiko

RUN \
  pip3 install --user \
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

COPY ipython_config.py /etc/ipython/ipython_config.py
COPY init.sh /init.sh

VOLUME ["/notebooks", "/shakedown"]

EXPOSE 8787/tcp 8888/tcp

WORKDIR /notebooks

ENV PYTHONDONTWRITEBYTECODE 1
ENV PATH /root/.local/bin:$PATH

ENTRYPOINT ["/bin/sh", "/init.sh"]