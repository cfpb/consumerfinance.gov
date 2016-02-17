# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "CentOS64"
  config.vm.box_url = "http://puppet-vagrant-boxes.puppetlabs.com/centos-64-x64-vbox4210.box"

  config.vm.network "forwarded_port", guest: 8000, host: 8080
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
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
