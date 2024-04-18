# FireDocker

## Description

SecDocker acts as an application firewall, monitoring and filtering Docker commands to prevent unauthorized or potentially harmful actions, thereby enhancing the security posture of CI environments without impeding development efficiency. We have updated the codebase to remove deprecated library features and implemented new ones, we have made better integration with the docker daemon and validated the JSON config configurations.

We focused on one of the main ideas of the paper: to restrict certain images from being used to create containers. 

## Research

Our research is based on [SecDocker](https://doi.org/10.1007/s42979-021-00939-4) [1], a concept proposed by researchers at the University of León. The paper introduces SecDocker, a tool designed to enhance cybersecurity in Continuous Integration (CI) workflows by addressing security vulnerabilities inherent in Docker-based containerization. SecDocker acts as an application firewall, monitoring and filtering Docker commands to prevent unauthorized or potentially harmful actions, thereby enhancing the security posture of CI environments without impeding development efficiency. SecDocker distinguishes itself through its modular, extensible architecture, crafted in Go.

SecDocker is presented as a possible solution to threats in CI pipelines by presenters at the [2023 USENIX Security Symposium](https://www.usenix.org/conference/usenixsecurity23/presentation/muralee) [2]. While the authors agree the work of SecDocker is promising, they report that it may require significant changes to existing CI infatstrucutre. However, these concepts could be build into new development pipelines.

### Our Contribution

We ran into issues replicating the results of the original SecDocker researchers. First, several of the plugins used were outdated. This led to stability issues with TCP connections. We were also unable to receive any http responses or interact with Docker containers as described in the paper.

We improved upon this by updating the codebase to function as a command line tool focusing on restricting container creation. We opted to switch from Go to Python due to the extensive support for Python within the Docker community. The packages we used are up-to-date and are able to interact with the Docker API as expected. We are able to evaluate Docker contain creation requests. If they are found to be valid, the containers can be created. If they do not meet specifications, creation will be denied.

[1] D. Fernández González, F. J. Rodríguez Lera, G. Esteban, and C. Fernández Llamas, "SecDocker: Hardening the Continuous Integration Workflow," SN Computer Science, vol. 3, no. 1, p. 80, Nov. 2021. [Online]. Available: <https://doi.org/10.1007/s42979-021-00939-4>

[2] S. Muralee, I. Koishybayev, A. Nahapetyan, G. Tystahl, B. Reaves, A. Bianchi, W. Enck, A. Kapravelos, and A. Machiry, "ARGUS: A Framework for Staged Static Taint Analysis of GitHub Workflows and Actions," in 32nd USENIX Security Symposium (USENIX Security 23), Anaheim, CA, Aug. 2023, pp. 6983-7000. [Online]. Available: <https://www.usenix.org/conference/usenixsecurity23/presentation/muralee>

## Requirements

You will need to install [Docker](https://www.docker.com/get-started/). Docker Desktop will need to be running in the background while running this program.

FireDocker can be run on Linux, MacOS, or on Windows with WSL. It can simply be run as described below on Linux or MacOS. To run on Windows, follow these instructions to set up WSL:

1. Install WSL:

    ```bash
    wsl --install
    ```

2. Create a username
3. Create a password
4. Run the program through WSL terminal.
5. Ensure Docker is configured to run on the WSL2 engine. [Instructions](https://docs.docker.com/desktop/wsl/)

Note: May need to clear return characters in script files in Windows using the following command:

```bash
sudo sed -i 's/\r//' <path/to/scriptName>
```

## How to Clone

```bash
    git clone https://github.com/racheljewell/FireDocker.git
```

## How to build/deploy (Windows)

Once Ubuntu installs for Windows or cloned for other machines, make sure Docker desktop is running.

In a new terminal:

```bash
    wsl --set-default ubuntu
```

To start Ubuntu:

```bash
    wsl
```

Clone the FireDocker Repo with: 

```bash
    git clone https://github.com/racheljewell/FireDocker.git
```

```bash
    cd FireDocker
```

# Run the script setup.sh 

```bash
    sudo bash setup.sh
```

# Verifying a connection with Docker:

```bash
    docker
```


## Functionality

### Help Command

Displays helpful hints on each of the commands. 

```bash
    firedocker --help
```

### To create a container

Then run

```bash
    firedocker --create <path to json config>
```

NOTE: You must have the specified image type installed on your machine in order to create the image. This  can be done by searching for the image in Docker Desktop and pulling it. See Docker API for examples of how to create json with image and other key value pairs. 

To make sure the container was created:

```bash
    firedocker --list
```

You should see seven labels followed by your newly created container

### To start a container

To see the name of your container:

```bash
    firedocker --list
```

To start the container:

```bash
    firedocker --start "<name of your container>"
```

To check if working as intended:

```bash
    firedocker --list
```

The status section should say "UP" followed by how long it has been up for

### To stop a container

To see the name of your container:

```bash
    firedocker --list
```

To stop the container:

```bash
    firedocker --stop "<name of your container>"
```

To check if working as intended:

```bash
    firedocker --list
```

The status section should say "Exited (0)" followed by how long ago it was exited

### To rename a container

To see the name of your container:

```bash
    firedocker --list
```

To rename the container:

```bash
    firedocker --rename "<name of your container>" "<name you want to rename it to>"
```

To check if working as intended:

```bash
    firedocker --list
```

Your container should now have the new name

### To list out your containers

```bash
    firedocker --list
```

You should now see a list of your containers

### To delete a container

To see the name of your container:

```bash
    firedocker --list
```

To delete the container:

```bash
    firedocker --delete "<name of your container>"
```

To check if working as intended:

```bash
    firedocker --list
```

Your container should no longer exist
