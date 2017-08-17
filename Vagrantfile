# -*- mode: ruby -*-
# vi: set ft=ruby :

# Install any required plugins
required_plugins = ['vagrant-hostmanager','vagrant-auto_network']

for plugin in required_plugins
  unless Vagrant.has_plugin? plugin
    system("vagrant plugin install #{plugin}")
    need_vagrant_up = true
  end
end

if need_vagrant_up
  puts 'Vagrant plugins have been modified -- Please re-run vagrant up'
  exit(1)
end

# Configure Vagrant-Auto_Network plugin settings
AutoNetwork.default_pool = '10.10.10.0/24'

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.vm.synced_folder '.', '/vagrant', sshfs: true
  config.vm.hostname = "cfpb.devel"
  config.vm.box = "CFPBCentOS64"
  config.vm.box_url = "https://s3.amazonaws.com/virtual-boxes/package.box"

  config.vm.network :private_network, :auto_network => true

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
