# FireDocker

## Description

SecDocker acts as an application firewall, monitoring and filtering Docker run commands to prevent unauthorized or potentially harmful actions, thereby enhancing the security posture of CI environments without impeding development efficiency. We have updated the codebase to remove deprecated library features and implemented new ones, we have made better integration with the docker daemon and validated the YAML configurations.

## Requirements

You will need to install [Docker](https://www.docker.com/get-started/)

FireDocker can be run on Linux, MacOS, or on Windows with WSL. It can simply be run as described below on Linux or MacOS. To run on Windows, follow these instructions to set up WSL:

1. Install WSL:

    ```bash
    wsl --install
    ```

2. Create username
3. Create password
4. Run program through WSL terminal.
5. Ensure docker is configured to run on the WSL2 engine. [Instructions](https://docs.docker.com/desktop/wsl/)

Note: May need to clear return characters in script files in Windows using the following command:

```bash
sudo sed -i 's/\r//' <path/to/scriptName>
```

## How to Clone

```bash
    git clone https://github.com/racheljewell/FireDocker.git
```

## How to build/deploy

Once ubuntu installs for windows or cloned for other machines, make sure docker desktop is running.

In a new terminal:
```bash
    wsl --set-default ubuntu
```

To start ubuntu:

```bash
    wsl
```
To get to where your clone is saved:

```bash
    cd /mnt
```
```bash
    cd c
```

Then cd to where your clone is

Establish connection with Docker:

```bash
    docker
```
To create an empty container:

```bash
    sudo python3 script.py --create config_test.json
```

Enter your password


## Functionality

#### To create a container

Go to docker_requests.py and change the debug to "True" and save.

Then run 
```bash
    python3 secdocker.py --create
```

You will be given an "This is a request" prompt followed by an error. Ignore this error.

Change the debug to "False" and save.

To make sure container was created: 
```bash
    docker ps -a
```
You should see seven labels followed by your newly created container

#### To start a container 

To see the name of the container created:
```bash
    docker ps -a
```
To start the coontainer:
```bash
    python3 secdocker.py --start "<name of your container>"
```
To check if working as intended:
```bash
    docker ps -a
```
the status section should say UP with 

#### To stop a container 

To see the name of the container created:
```bash
    docker ps -a
```
To stop the coontainer:
```bash
    python3 secdocker.py --stop "<name of your container>"
```
To see it running:
```bash
    docker ps -a
```
