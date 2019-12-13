FROM jenkins/jenkins:lts

# if we want to install via apt
USER root

RUN  \
  apt update && \
  apt install -y build-essential && \
  apt install -y python3 python3-dev && \
  apt install -y python3-pip python3-paramiko && \
  apt install -y python-pip && \
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
  pip3 install git+https://github.com/arista-northwest/eapi-py.git && \
  pip3 install git+https://github.com/arista-northwest/shakedown.git && \
  pip install tox

# COPY bin/sdtest /usr/local/bin/sdtest
# RUN chmod +x /usr/local/bin/sdtest

# COPY job-template.xml /var/jenkins_home/jobs/Shakedown-Template/config.xml
COPY job-template.xml /var/tmp/job-template.xml

VOLUME ["/testplan", "/shakedown", "/reports"]

EXPOSE 8080/tcp 50000/tcp

USER jenkins

RUN /usr/local/bin/install-plugins.sh \
  git github-branch-source python jdk-tool command-launcher \
  bouncycastle-api filesystem_scm credentials

# RUN cat /var/tmp/job-template.xml | \
# java -jar /var/jenkins_home/war/WEB-INF/jenkins-cli.jar \
#   -s http://localhost:8080/ create-job Shakedown-Template

ENV PYTHONPATH /shakedown
ENV PYTHONDONTWRITEBYTECODE 1
ENV JAVA_OPTS "-Djava.awt.headless=true -Djenkins.install.runSetupWizard=false"
