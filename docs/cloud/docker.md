# docker :material-docker:

??? Resources
    * [:material-docker: Docker docs](https://docs.docker.com/)! The starting point
    * [:material-youtube: Docker and Kubernetes complete tutorial](https://www.youtube.com/playlist?list=PL0hSJrxggIQoKLETBSmgbbvE4FO_eEgoB), a very detailed playlist from beginner to advanced level in both Docker and Kubernetes - it's also a [:fontawesome-solid-book: Udemy course](https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/), by the way
    * [:material-youtube: Dev containers](https://www.youtube.com/playlist?list=PLj6YeMhvp2S5G_X6ZyMc8gfXPMFPg3O31), a playlist from the VS Code YouTube channel about containerized dev environments
    * [:fontawesome-solid-euro-sign: Docker Mastery](https://www.udemy.com/course/docker-mastery/) Udemy course on Docker and Kubernetes, by a Docker Captain
    * [15 Quick Docker Tips](https://www.ctl.io/developers/blog/post/15-quick-docker-tips)

![docker-moby](https://www.docker.com/sites/default/files/Whale%20Logo332_5.png)

## Concepts

* Docker takes advantage of the kernel's property of **namespacing** (isolating resources per process or group of processes, e.g. when a process needs a specific portion of the actual hardware such as the hard drive, but not the rest) and **control groups (cgroups)** (limiting the amount of resources - RAM, CPU, HD I/O, network bandwith, etc. per process or group of processes)

![docker-namespacing](http://vicch.github.io/pkb/programming/images/docker_and_kubernetes/04.png)

* So a **container** is basically a process whose system calls are redirected to a namespaced portion of dedicated hardware (HD, RAM, network, CPU, etc.) through the host's kernel

![docker-container](http://vicch.github.io/pkb/programming/images/docker_and_kubernetes/05.png)

* An **image** is essentially a filesystem snapshot with a startup command

![docker-image](http://vicch.github.io/pkb/programming/images/docker_and_kubernetes/06.png)

* Docker's architecture:

![components-of-docker-engine](https://docs.docker.com/engine/images/architecture.svg)


## Install docker on Debian 

Reference [:material-docker: here](https://docs.docker.com/engine/install/debian/))

* Compare your Debian version (in `/etc/issue`) with the current [:material-docker: installation requirements](https://docs.docker.com/engine/install/debian/#os-requirements)
* Set up the stable Docker repository with 
```bash
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release
sudo curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
sudo echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
* Install the Docker engine:
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```
* Test the installation with:
```bash
docker --version
```
* Create a new user group called 'docker' and add your user to it:
```bash
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```
Test the last commands by running `docker` without having to preface `sudo`.
* Configure Docker to start on boot:
```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
```

## Administration

### Images and containers

* `docker image ls`: all the images in the docker host's cache
* `docker container ls -al`: all the containers with all the statuses (running, created, exited, stopped, etc)

* `docker container run --detach --name postgres14 --publish 5432:5432 --env POSTGRES_USER=root --env POSTGRES_PASSWORD=secretpassword postgres:14-alpine`: runs a new detached instance of the `postgres:14-alpine` image by publishing the container's port `5432` and using the specified environment variables

* `docker container run --interactive --tty --name ubuntu ubuntu bash`: will overwrite the startup command included with the `ubuntu:latest` image with the `bash` command, thus opening an interactive pseudo-tty shell

* `docker image prune --all`: deletes all [:material-stack-overflow: dangling images](https://stackoverflow.com/a/45143234), check before deleting with `docker images --filter "dangling=true"`

!!! info
    **How to pull the image of a specific distro (es. Alpine) without specifying the tag version?** (:warning: to be tested): get all the tags of a specific `image` in a list (you will need the JSON processor [jq](https://stedolan.github.io/jq/), just use `apt-get install jq`) and filtering them by distro with `grep`:
    ```bash
    wget -q https://registry.hub.docker.com/v1/repositories/postgres/tags -O - | jq -r '.[].name' | grep '\-alpine'
    ```
    Replace `postgres` with your image name

* `docker container cp FILE CONTAINER_NAME:/`: it copies `FILE` in the root folder of the `CONTAINER_NAME`

* `docker container stop CONTAINER_NAME_OR_ID`: it sends a `SIGTERM` signal to the primary process inside the container, letting it shut down on its own time and with its own clean-up procedure

* `docker container kill CONTAINER_NAME_OR_ID`: it sends a `SIGKILL` signal to the primary process inside the container, shutting it down _immediately_; it's automatically used by the Docker Server if the container's process does not respond to the `docker stop` command within 10 seconds. 

* `docker system prune`: it removes all stopped containers, all networks not used, all dangling images, all build cache

* Get the docker image ID by its name (`IMAGE-NAME`):
```bash
docker images --format="{{.Repository}} {{.ID}}" |      # Reformat the output of 'docker images'
grep "IMAGE-NAME" |         # Find your image
cut -d' ' -f2               # Cut the output and pick the ID
```

* [Remove all Exited containers](https://coderwall.com/p/zguz_w/docker-remove-all-exited-containers): it may occur that some containers with running processes are in the `Exited` status and therefore won't be deleted with the `docker container rm` command - or, the specific ID will be removed and immediately replaced with another one. Then just run:
```bash
docker rm $(docker ps -a -f status=exited -q)
```

### Network drivers and aliases

Reference [:material-docker: here](https://docs.docker.com/engine/tutorials/networkingcontainers/).

* `docker network ls`: all the networks in docker

> :warning: Remember that the `bridge` default network does not support the internal DNS - which you can find in any new bridge network created with `docker network create --driver bridge NETWORK`. So, it's a best practice to always create your custom networks and attach your containers to them (with `docker network connect NETWORK CONTAINER`). 

* `docker network inspect --format "{{json .Containers }}" bridge | jq`: lists all the containers connected to the default docker network `bridge`

* `docker network inspect --format "{{json .IPAM.Config }}" bridge | jq` : gives the IP range used by the default docker network `bridge`

* `docker container inspect --format "{{json .NetworkSettings.IPAddress }}" nginx | jq` : the `nginx` container's internal IP address read from the `inspect` output (:warning: use the container's hostname instead of IP address... containers _really are_ ephemeral!)

* `docker network connect NETWORK CONTAINER --alias ALIAS`: will set the `ALIAS` of the container in the network. 

> Multiple containers can even have the same alias. That's used for [:material-wiki: DNS Round-Robin](https://en.wikipedia.org/wiki/Round-robin_DNS), a form of DNS-based load-balacing test.

!!! note "Using a `makefile` to speed up the docker commands"

    To avoid typing long bash commands, automate the most usual ones with a [Makefile](https://www.gnu.org/software/make/manual/make.html) (also a tutorial at [Makefiletutorial](https://makefiletutorial.com/)). The Makefile follows the syntax:
    ```bash
    target: prerequisites
        command
        command
        command
    ```
    Therefore an example of handling database migrations on a [PostgreSQL](./../db/postgres.md) container would be:
    ```bash
    # Variables
    containername = YOUR-CONTAINER-NAME
    dbname = YOUR-DB-NAME
    dbuser = YOUR-DB-USER
    dbpassword = YOUR-DB-PASSWORD

    runbash: # It opens a bash shell on the target container
        sudo docker exec -it $(containername) bash

    runpostgres: # It runs a PostgreSQL container
        sudo docker run -d --name $(containername) -p 54325:5432 -e POSTGRES_DB=root -e POSTGRES_USER=$(dbuser) -e POSTGRES_PASSWORD=$(dbpassword) postgres:14-alpine

    createdb: # It creates the PostgreSQL database in the container
        sudo docker exec -it $(containername) createdb --username=$(dbuser) --owner=$(dbuser) $(dbname)

    dropdb: # It drops the PostgreSQL database in the container
        sudo docker exec -it $(containername) dropdb $(dbname)

    migrateup: # It performs a forward db migration
        migrate -path db/migrations -database "postgresql://$(dbuser):$(dbpassword)@localhost:54325/$(dbname)?sslmode=disable" -verbose up

    migratedown: # It performs a backward db migration
        migrate -path db/migrations -database "postgresql://$(dbuser):$(dbpassword)@localhost:54325/$(dbname)?sslmode=disable" -verbose down	

    runpsql: # It opens a psql shell on the target container
        sudo docker exec -it $(containername) psql $(dbname)

    .PHONY: runbash runpostgres createdb dropdb runpsql migrateup migratedown
    ```
    Then quickly recall the commands with `make`! 🎉🎊 For example:
    ```bash
    make runbash    # It will open a bash shell on the specified container
    ```
    For instance, to quickly set up your new containerized database, just:
    ```bash
    make runpostgres # Create the container and start it
    make createdb # Create the database
    make migrateup # Run the first migration to create the schema
    make runpsql # Start the psql CLI
    ```
    :warning: Watch out for tabs in the Makefile, as explained in [:material-stack-overflow: this StackOverflow answer](https://stackoverflow.com/a/16945143). Use `cat -etv Makefile` to look for missing tabs (`^I`).

## Troubleshooting

> Learn on a running container: `docker run -d IMAGE_NAME ping google.com`, where the `ping google.com` command overrides the default image's startup command and leaves the container always running

!!! warning
    The error **docker: Error response from daemon: driver failed programming external connectivity on endpoint ...: Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use** means that the specified local port (i.e. in the example, the bind `0.0.0.0:5432`) is already used by another process... Just change the host port :ok_hand:.

* `docker container exec --interactive --tty postgres14 psql -U root`: it will start a command (the one specified after the image's name, here `psql -U root`) running _in addition_ to the startup command

* `docker container logs CONTAINER_NAME_OR_ID`: it shows the logs of the specified `CONTAINER_NAME_OR_ID`. This is the same output as running the container without the `--detach` flag.

## Developing

An example of Dockerfile for a Python application (references [:material-docker: here](https://docs.docker.com/language/python/build-images/)):

```dockerfile
# syntax=docker/dockerfile:1

# Base image
FROM python:3.8-slim-buster

# Container's default location for all subsequent commands
WORKDIR /app

# Copy command from the Dockerfile local folder to the path relative to WORKDIR 
COPY requirements.txt requirements.txt

# Running a command with the image's default shell (it can be changed with a SHELL command)
RUN pip3 install -r requirements.txt

# Copy the whole source code
COPY . .

# Command we want to run when our image is executed inside a container
# Notice the "0.0.0.0" meant to make the application visible from outside of the container
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
```

* `CMD` arguments can be over-ridden:
```dockerfile
cat Dockerfile
FROM ubuntu
CMD ["echo"]
$ docker run imagename echo hello
hello
```
`ENTRYPOINT` arguments can NOT be over-ridden:
```dockerfile
cat Dockerfile
FROM ubuntu
ENTRYPOINT ["echo"]
$ docker run imagename echo hello
echo hello
```

* To install an unpacked service using its executable on Docker, use the following Dockerfile:
```
FROM mcr.microsoft.com/windows/servercore:ltsc2019
WORKDIR /app
COPY . "C:/app"
RUN ["C:/Windows/Microsoft.NET/Framework/v4.0.30319/InstallUtil.exe", "/i", "EXECUTABLE_NAME.exe"]
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]
CMD c:\app\Wait-Service.ps1 -ServiceName 'SERVICE_NAME' -AllowServiceRestart
```
Where the `Wait-Service.ps1` script is [:material-github: here](https://github.com/MicrosoftDocs/Virtualization-Documentation/blob/main/windows-server-container-tools/Wait-Service/Wait-Service.ps1).


