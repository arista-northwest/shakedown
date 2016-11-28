# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/xenial32"
  config.vm.network "forwarded_port", guest: 8000, host: 8008
  config.vm.synced_folder "./notebooks", "/notebooks"
  config.vm.provision "shell", inline: $script
end

$script = <<SCRIPT
#!/bin/bash

apt-get update
# apt-get upgrade -y

apt-get install -y build-essential libssl-dev libffi6 libffi-dev
apt-get install -y libfreetype6 libfreetype6-dev pkg-config
apt-get install -y python3.5 python3.5-dev python3-pip libncurses5-dev

pip3 install --upgrade pip
pip3 install jinja2 pyyaml
pip3 install cryptography --force-reinstall
pip3 install requests sh paramiko
pip3 install numpy scipy matplotlib ipython jupyter pandas sympy nose

# pip3 install arcomm
pip3 install --upgrade git+https://github.com/aristanetworks/arcomm.git

cd /vagrant; python3 setup.py develop

###################
# BEGIN: JupyterHub
###################
apt-get install -y npm nodejs-legacy
npm install -g configurable-http-proxy
pip3 install jupyterhub
pip3 install git+https://github.com/jupyter/sudospawner

# Notes:
#
# https://github.com/jupyterhub/jupyterhub/wiki/Run-jupyterhub-as-a-system-service
# https://github.com/jupyterhub/jupyterhub/wiki/Using-sudo-to-run-JupyterHub-without-root-privileges

mkdir /etc/jupyterhub /etc/ipython
# chown jupyterhub /etc/jupyterhub

cat > /etc/jupyterhub/jupyterhub_config.py <<EOF
c.JupyterHub.confirm_no_ssl = True
c.JupyterHub.ip = '0.0.0.0'
c.JupyterHub.spawner_class='sudospawner.SudoSpawner'
c.Spawner.notebook_dir = '/notebooks'
EOF

cat > /etc/ipython/ipython_config.py <<EOF
c.InteractiveShellApp.extensions = ['arcomm.ipython.magics', 'shakedown.magics']
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
usermod -a -G jupyterhub ubuntu
systemctl daemon-reload
systemctl start jupyterhub.service

#################
# END: JupyterHub
#################

# install/setup supporting services
apt-get install -y ntp dnsmasq
# apt-get install -y syslog-ng syslog-ng-core tacacs+ nginx

# if ! grep -q shakedown /etc/hosts; then
#
#     cat >> /etc/hosts <<EOF
# 192.168.56.7 shakedown
# 172.16.128.101 sdf veos-sdf-01
# 172.16.128.102 ord veos-ord-01
# 172.16.128.103 den veos-den-01
# 172.16.128.104 sea veos-sea-01
# EOF
# fi
#
# cat > /etc/ntp.conf <<EOF
# driftfile /var/lib/ntp/ntp.drift
# statistics loopstats peerstats clockstats
# filegen loopstats file loopstats type day enable
# filegen peerstats file peerstats type day enable
# filegen clockstats file clockstats type day enable
# server 0.ubuntu.pool.ntp.org iburst
# server 1.ubuntu.pool.ntp.org iburst
# server 2.ubuntu.pool.ntp.org iburst
# server 3.ubuntu.pool.ntp.org iburst
# server ntp.ubuntu.com
# restrict -4 default kod notrap nomodify nopeer noquery
# restrict -6 default kod notrap nomodify nopeer noquery
# restrict 127.0.0.1
# restrict ::1
# restrict 0.0.0.0 mask 0.0.0.0 modify notrap
# EOF
#
# cat > /etc/dnsmasq.d/local.conf <<EOF
# local=/shakedown/
# expand-hosts
# domain=shakedown
# EOF
#
# cat > /etc/tacacs+/tac_plus.conf <<EOF
# key = "shakedown"
# accounting file = /var/log/tac_plus.acct
#
# group = admins {
#     default service = permit
#     service = exec {
#         priv-lvl = 15
#     }
# }
#
# group = rousers {
#     default service = permit
#     service = exec {
#         priv-lvl = 1
#     }
# }
#
# user = admin {
#     member = admins
#     login = nopassword
# }
#
# user = shakedown {
#     member = admins
#     login = cleartext shakedown
# }
#
# user = rouser {
#     member = rouser
#     login = cleartext nocuser
# }
# EOF
#
# cat > /etc/syslog-ng/conf.d/network.conf <<EOF
# options { keep_hostname(yes); };
# source s_net { tcp(); udp(); };
# filter f_lessnoisy { not (
#         message("LINEPROTO")
#         or message("SPANTREE")
#     );
# };
# destination d_net { file("/var/log/network"); };
# # uncomment this line (and comment out the next one) to discard noisy logs messages
# #log { source(s_net); filter(f_lessnoisy); destination(d_net); };
# log { source(s_net); destination(d_net); };
# EOF

SCRIPT
