# Installation and Congiguration for cfgov-refersh with Vagrant

## 1. Environment Varaibles setup

The project uses a number of environment variables.
The `setup.sh` script will create a `.env` file for you
from the `.env_SAMPLE` file found in the repository,
if you don't already have one.

Inside the `.env` file you can customize the project environment configuration.

If you would like to manually copy the environment settings,
copy the `.env_SAMPLE` file and un-comment each variable after
adding your own values.
```bash
cp -a .env_SAMPLE .env && open .env
```

Then load the environment variables with:
```bash
. ./.env
```

## 2. Fetch extra playbooks

The project pulls together various open source and closed source plays. The plays are
managed through ansible-galaxy, a core module for this exact purpose. To download all
the dependencies, there is a simple command.

```bash
ansible-galaxy install -r ansible/requiremenst.yml
```

## 3. Vagrant up

The project uses vagrant to create the simulated virtual environment allowing the developer
to work on a production like environment while maintaining development work on the
local machine. To create this virtual environment, you need to execute the following command and please
be patient the first time you run this step.

```bash
vagrant up
```


## 4. Frontend Tools

In order to run the application, we must generate the front end assets. After running these commands, simply visit http://localhost:8001. You can also place the two export commands into your .bashrc to simplify things later. 

```bash
export CFGOV_HOME=path/to/cfgov-refresh
export PATH=$PATH:$CFGOV_HOME/bin
cfgov init
cfgov assets
cfgov django start
```



