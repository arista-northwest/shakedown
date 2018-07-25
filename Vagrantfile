# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial32"
  config.vm.network "private_network", type: "dhcp"
  config.vm.network "forwarded_port", guest: 8000, host: 8008
  config.vm.network "forwarded_port", guest: 5000, host: 5008
  config.vm.network "forwarded_port", guest: 8080, host: 8080
  config.vm.network "forwarded_port", guest: 50000, host: 50000
  config.vm.synced_folder "./examples", "/examples",
    mount_options: ["dmode=777", "fmode=666"]
  config.vm.provision "shell", inline: $script
end

$script = <<SCRIPT
#!/bin/bash

apt-get update
# apt-get upgrade -y

apt-get install -y build-essential libssl-dev libffi6 libffi-dev
apt-get install -y libfreetype6 libfreetype6-dev pkg-config libncurses5-dev

add-apt-repository -y ppa:jonathonf/python-3.6
apt-get update
apt-get install -y python3.6 python3.6-dev python3.6-venv

wget https://bootstrap.pypa.io/get-pip.py
python3.6 get-pip.py
rm -f get-pip.py

pip3 install cryptography --force-reinstall
pip3 install requests sh paramiko
# see: https://github.com/jupyter/notebook/issues/3397
pip3 install tornado==4.5.3
pip3 install jupyter
# pip3 install numpy scipy matplotlib pandas sympy nose

pip3 install -r /vagrant/requirements.txt

cd /vagrant; python3.6 setup.py develop; cd ~

# # setup go/gnmi
# wget https://dl.google.com/go/go1.10.3.linux-386.tar.gz
# tar zxvf go1.10.3.linux-386.tar.gz -C /usr/local/
# sudo -i -u vagrant go get github.com/aristanetworks/goarista/cmd/gnmi

###################
# Jenkins
###################
apt install openjdk-8-jre
apt install jenkins

###################
# BEGIN: JupyterHub
###################
apt-get install -y npm nodejs-legacy
npm install -g configurable-http-proxy
pip3 install jupyterhub==0.8.1
#pip3 install jupyterhub-dummyauthenticator
pip3 install git+https://github.com/jupyter/sudospawner

# Notes:
#
# https://github.com/jupyterhub/jupyterhub/wiki/Run-jupyterhub-as-a-system-service
# https://github.com/jupyterhub/jupyterhub/wiki/Using-sudo-to-run-JupyterHub-without-root-privileges

mkdir /etc/jupyterhub /etc/ipython

cat > /etc/jupyterhub/jupyterhub_config.py <<EOF
c.JupyterHub.confirm_no_ssl = True
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.spawner_class='sudospawner.SudoSpawner'
c.Spawner.notebook_dir = '/examples'
c.PAMAuthenticator.open_sessions = False
#c.JupyterHub.authenticator_class = 'dummyauthenticator.DummyAuthenticator'
EOF

cat > /etc/ipython/ipython_config.py <<EOF
c.InteractiveShellApp.extensions = ['shakedown.ipython.magics']
EOF

cat > /lib/systemd/system/jupyterhub.service <<EOF
[Unit]
Description=Jupyterhub
After=network-online.target

[Service]
User=jupyterhub
ExecStart=/usr/local/bin/jupyterhub -f /etc/jupyterhub/jupyterhub_config.py
WorkingDirectory=/var/jupyterhub

[Install]
WantedBy=multi-user.target
EOF

if ! grep -q JUPYTER_CMD /etc/sudoers; then
    cat >> /etc/sudoers <<EOF
Cmnd_Alias JUPYTER_CMD = /usr/local/bin/sudospawner
jupyterhub ALL=(%jupyterhub) NOPASSWD:JUPYTER_CMD
EOF

fi

mkdir /var/jupyterhub
useradd jupyterhub
chown jupyterhub /var/jupyterhub
usermod -a -G shadow jupyterhub
useradd -G jupyterhub -m shakedown
echo "shakedown:shakedown" | chpasswd
systemctl daemon-reload
systemctl enable jupyterhub.service
systemctl start jupyterhub.service

#################
# END: JupyterHub
#################

cat >> /etc/hosts <<EOF
192.168.56.11 veos-1 veos-1.lab.lan
192.168.56.12 veos-2 veos-2.lab.lan
192.168.56.13 veos-3 veos-3.lab.lan
192.168.56.14 veos-4 veos-4.lab.lan
EOF


#################
# Uncomment for local lab...
#################
# install/setup supporting services
apt-get install -y ntp dnsmasq
apt-get install -y syslog-ng syslog-ng-core tacacs+ nginx

if ! grep -q shakedown /etc/hosts; then

    cat >> /etc/hosts <<EOF
192.168.56.7 shakedown
172.16.128.101 sdf veos-sdf-01
172.16.128.102 ord veos-ord-01
172.16.128.103 den veos-den-01
172.16.128.104 sea veos-sea-01
EOF
fi

cat > /etc/ntp.conf <<EOF
driftfile /var/lib/ntp/ntp.drift
statistics loopstats peerstats clockstats
filegen loopstats file loopstats type day enable
filegen peerstats file peerstats type day enable
filegen clockstats file clockstats type day enable
server 0.ubuntu.pool.ntp.org iburst
server 1.ubuntu.pool.ntp.org iburst
server 2.ubuntu.pool.ntp.org iburst
server 3.ubuntu.pool.ntp.org iburst
server ntp.ubuntu.com
restrict -4 default kod notrap nomodify nopeer noquery
restrict -6 default kod notrap nomodify nopeer noquery
restrict 127.0.0.1
restrict ::1
restrict 0.0.0.0 mask 0.0.0.0 modify notrap
EOF

cat > /etc/dnsmasq.d/local.conf <<EOF
local=/shakedown/
expand-hosts
domain=shakedown
EOF

cat > /etc/tacacs+/tac_plus.conf <<EOF
key = "shakedown"
accounting file = /var/log/tac_plus.acct

group = admins {
    default service = permit
    service = exec {
        priv-lvl = 15
    }
}

group = rousers {
    default service = permit
    service = exec {
        priv-lvl = 1
    }
}

user = admin {
    member = admins
    login = nopassword
}

user = shakedown {
    member = admins
    login = cleartext shakedown
}

user = rouser {
    member = rouser
    login = cleartext nocuser
}
EOF

cat > /etc/syslog-ng/conf.d/network.conf <<EOF
options { keep_hostname(yes); };
source s_net { tcp(); udp(); };
filter f_lessnoisy { not (
        message("LINEPROTO")
        or message("SPANTREE")
    );
};
destination d_net { file("/var/log/network"); };
# uncomment this line (and comment out the next one) to discard noisy logs messages
#log { source(s_net); filter(f_lessnoisy); destination(d_net); };
log { source(s_net); destination(d_net); };
EOF

SCRIPT
