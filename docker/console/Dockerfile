FROM ubuntu:latest

RUN  \
  apt-get update && \
  apt-get install -y build-essential && \
  apt-get install -y python3 python3-dev && \
  apt-get install -y python3-pip python3-paramiko && \
  apt-get install -y python-pip && \
  apt-get install -y git && \
  apt-get install -y sshpass && \
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
  pip3 install git+https://github.com/arista-northwest/eapi-py.git && \
  pip3 install git+https://github.com/aristanetworks/arcomm.git && \

VOLUME ["/shakedown", "/testplan", "/reports"]

# COPY init.sh /init.sh

WORKDIR /testplan

ENTRYPOINT ["/bin/bash"]
