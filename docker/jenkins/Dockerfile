FROM jenkins/jenkins:lts

# if we want to install via apt
USER root

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
    # \
    #git+https://github.com/arista-northwest/shakedown.git
      

# COPY bin/sdtest /usr/local/bin/sdtest
# RUN chmod +x /usr/local/bin/sdtest

# COPY job-template.xml /var/jenkins_home/jobs/Shakedown-Template/config.xml
# COPY job-template.xml /var/tmp/job-template.xml

VOLUME ["/testplan", "/shakedown", "/reports"]

EXPOSE 8080/tcp 50000/tcp

USER jenkins

RUN jenkins-plugin-cli --plugins \
  git github-branch-source jdk-tool command-launcher \
  bouncycastle-api filesystem_scm credentials configuration-as-code job-dsl

ENV PYTHONPATH /shakedown
ENV PYTHONDONTWRITEBYTECODE 1
ENV CASC_JENKINS_CONFIG=/var/jenkins_home/casc
ENV JAVA_OPTS "-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false -Dsun.net.inetaddr.ttl=0"
