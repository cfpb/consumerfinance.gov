# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "CentOS64"
  config.vm.box_url = "http://puppet-vagrant-boxes.puppetlabs.com/centos-64-x64-vbox4210.box"

  config.vm.network "forwarded_port", guest: 8000, host: 8001
  config.vm.network "forwarded_port", guest: 3306, host: 3307
  config.vm.network "forwarded_port", guest: 9200, host: 9201
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
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
