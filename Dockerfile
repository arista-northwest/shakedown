FROM alpine:edge

RUN \
  apk update && \
  apk upgrade && \
  apk add bash && \
  apk add git && \
  apk add python3 && \
  apk add py3-pip py3-paramiko && \
  apk add alpine-sdk python3-dev freetype-dev && \
  pip3 install --upgrade pip && \
  pip3 install future && \
  pip3 install pytest && \
  pip3 install jinja2 && \
  pip3 install pyyaml && \
  pip3 install requests && \
  pip3 install sh && \
  pip3 install mistune && \
  pip3 install numpy matplotlib ipython jupyter pandas && \
  pip3 install cryptography --force-reinstall && \
  pip3 install git+https://github.com/aristanetworks/arcomm.git

RUN apk del alpine-sdk python3-dev freetype-dev

ADD . /shakedown

VOLUME ["/notebooks"]

ENV PYTHONPATH /shakedown

WORKDIR /notebooks

#ENTRYPOINT [""]
