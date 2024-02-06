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

RUN \
  pip install --user -U pipenv

ENV PATH /root/.local/bin:$PATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV LANG en_US.UTF-8

ADD . /shakedown
WORKDIR /shakedown

RUN \
  pipenv install --dev -e .
  # && \
  #echo "source $(pipenv --env)/bin/activate" >> ~/.bashrc

VOLUME ["/shakedown", "/testplan", "/reports"]

#WORKDIR /testplan

ENTRYPOINT [ "sleep", "infinity" ]

