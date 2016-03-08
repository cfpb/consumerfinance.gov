Using the vagrant machine
===

1) git clone xxxx
2) cd cfgov-refresh
3) ansible-galaxy install -r ansible/requiremenst.yml
4) setup your .env file
5) vagrant up
6) export CFGOV_HOME=path/to/cfgov-refresh
7) export PATH=$PATH:$CFGOV_HOME/bin
8) cfgov init
9) cfgov assets
10) cfogv django start
