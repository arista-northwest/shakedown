FROM ubuntu:latest

RUN  \
  apt update && \
  apt install -y build-essential && \
  apt install -y python3 python3-dev && \
  apt install -y python3-pip python3-paramiko && \
  apt install -y git && \
  apt install -y sshpass

RUN \
  pip3 install pandas numpy matplotlib && \
  pip3 install pexpect && \
  pip3 install future && \
  pip3 install pytest && \
  pip3 install jinja2 && \
  pip3 install pyyaml && \
  pip3 install requests && \
  pip3 install sh && \
  pip3 install mistune && \
  pip3 install tinydb && \
  pip3 install tinymongo && \
  pip3 install git+https://github.com/arista-northwest/eapi-py.git

RUN \
  pip3 install tornado==4.5.3 && \
  pip3 install jupyter

COPY ipython_config.py /etc/ipython/ipython_config.py
COPY init.sh /init.sh

VOLUME ["/notebooks", "/shakedown"]

EXPOSE 8787/tcp 8888/tcp

WORKDIR /notebooks

ENV PYTHONDONTWRITEBYTECODE 1

ENTRYPOINT ["/bin/sh", "/init.sh"]
