# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "CFPBCentOS64"
  config.vm.box_url = "https://s3.amazonaws.com/virtual-boxes/package.box"

  config.vm.network "forwarded_port", guest: 80, host: 8002
  config.vm.network "forwarded_port", guest: 8000, host: 8001
  config.vm.network "forwarded_port", guest: 3306, host: 3307
  config.vm.network "forwarded_port", guest: 9200, host: 9201

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

  config.vm.provision "ansible" do |ansible|
      ansible.playbook = "ansible/cfgov_refresh_setup.yml"
      ansible.verbose = 'v'
      ansible.groups = {
          "db" => ["default"],
          "app" => ["default"]
      }
  end
end
