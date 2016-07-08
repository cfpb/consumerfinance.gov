# cfgov-refresh docker installation

Before running the docker setup, you will need to install docker and docker-compose:
```
brew install docker docker-compose
```

On Mac and Windows, docker will need virtualbox to setup a docker machine.  This problem goes away in the [beta release](https://blog.docker.com/2016/03/docker-for-mac-windows-beta/) which is not currently supported with a brew install.
```
docker-machine create --driver virtualbox default
```
This creates a new docker machine and names it `default`.

To setup your shell environment, you will need to tell your shell about the docker machine:
```
eval "$(docker-machine env default)”
```
Consider adding this line to your .bashrc or .profile.

```
echo 'eval "$(docker-machine env default)"' >>~/.bashrc
```

Your docker-machine will have an ip address, which you can find out by typing:
```
docker-machine ip default
```

# Installation

To run/install cf-gov refresh please run:
```
docker-compose up
```

The initial setup will take approximately 35-40 minutes.

To view the website, please navigate to your docker machine's IP address on port 8000.

Ex.: `http://192.168.99.100:8000`

# Making code changes locally

After running `docker-compose up`, you should have a local folder apps/ with each of the optional cf-gov applications loaded.

These folders are not linked to any git repository.  You can link your local folder to your remote git repository using the standard: `git init` `git remote add` commands.

Any changes you make on your local codebase will be updated and visible on your web browser.  This includes changes to the python code, as well as gulp watch, and npm commands, etc.

Currently, front-end asset compilation is not working correctly inside the container, so that step will need to be run on your local machine.

Ex.: `./frontend.sh`



