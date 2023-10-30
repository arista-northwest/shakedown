FROM ubuntu:latest

RUN  \
  apt update && \
  apt install -y build-essential libffi-dev && \
  apt install -y python3 python3-dev && \
  apt install -y python3-pip python3-paramiko && \
  apt install -y git && \
  apt install -y sshpass

RUN \
  pip3 install nest_asyncio tornado jupyter

COPY ipython_config.py /etc/ipython/ipython_config.py
COPY init.sh /init.sh

VOLUME ["/notebooks", "/shakedown"]

EXPOSE 8787/tcp 8888/tcp

WORKDIR /notebooks

ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["/bin/sh", "/init.sh"]
