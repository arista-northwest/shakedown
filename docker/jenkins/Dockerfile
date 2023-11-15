FROM jenkins/jenkins:lts

# if we want to install via apt
USER root

RUN  \
  apt update && \
  apt install -y build-essential && \
  apt install -y python3 python3-dev python-is-python3 && \
  apt install -y python3-pip python3-paramiko && \
  apt install -y git && \
  apt install -y sshpass

RUN \
  pip3 install --break-system-packages pandas numpy matplotlib && \
  pip3 install --break-system-packages pexpect && \
  pip3 install --break-system-packages future && \
  pip3 install --break-system-packages pytest && \
  pip3 install --break-system-packages jinja2 && \
  pip3 install --break-system-packages requests && \
  pip3 install --break-system-packages sh && \
  pip3 install --break-system-packages mistune && \
  pip3 install --break-system-packages tinydb && \
  pip3 install --break-system-packages tinymongo && \
  pip3 install --break-system-packages eapi-py==0.4.1 && \
  pip3 install --break-system-packages git+https://github.com/arista-northwest/shakedown.git
  # && \
 RUN \
  pip3 install --break-system-packages tox

# COPY bin/sdtest /usr/local/bin/sdtest
# RUN chmod +x /usr/local/bin/sdtest

# COPY job-template.xml /var/jenkins_home/jobs/Shakedown-Template/config.xml
COPY job-template.xml /var/tmp/job-template.xml

VOLUME ["/testplan", "/shakedown", "/reports"]

EXPOSE 8080/tcp 50000/tcp

USER jenkins

RUN jenkins-plugin-cli --plugins \
  git github-branch-source jdk-tool command-launcher \
  bouncycastle-api filesystem_scm credentials

# RUN cat /var/tmp/job-template.xml | \
# java -jar /var/jenkins_home/war/WEB-INF/jenkins-cli.jar \
#   -s http://localhost:8080/ create-job Shakedown-Template

ENV PYTHONPATH /shakedown
ENV PYTHONDONTWRITEBYTECODE 1
ENV JAVA_OPTS "-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false"
