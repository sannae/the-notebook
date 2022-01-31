# docker :material-docker:

!!! Resources
    * [:material-docker: Docker docs](https://docs.docker.com/)! The starting point
    * [:material-youtube: Dev containers](https://www.youtube.com/playlist?list=PLj6YeMhvp2S5G_X6ZyMc8gfXPMFPg3O31), a playlist from the VS Code YouTube channel about containerized dev environments

## Getting started

### Install docker on Debian (ref. [:material-docker: here](https://docs.docker.com/engine/install/debian/))

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

## Architecture

* Container virtualization layers:
![container-virtualization-layers](https://docs.microsoft.com/en-us/learn/modules/intro-to-docker-containers/media/5-efficient-use-hardware.svg)

* Components of the Docker Engine:
    * **docker client**: a CLI-based application named `docker` to interact with the local or remote Docker server via the Docker REST API. 
    * **docker server** or **docker daemon**: a daemon named `dockerd`, responding to requests from the client via the Docker REST API and interacting with other daemons.
![components-of-docker-engine](https://docs.microsoft.com/en-us/learn/modules/intro-to-docker-containers/media/2-docker-architecture.svg)

* Container lifecycle:
![container-lifecycle](https://docs.microsoft.com/en-us/learn/modules/intro-to-docker-containers/media/4-docker-container-lifecycle.svg)

## Help

### Basics

* `docker ps -a`: list all containers and their statuses

* `docker images ls`: list all images
* `docker images prune --all`: deletes all [:material-stack-overflow: dangling images](https://stackoverflow.com/a/45143234), check before deleting with `docker images --filter "dangling=true"`
* `docker pull IMAGE-NAME:TAG`: it downloads the image with the specified name (and the specified `TAG`, or `latest` if not specified) from the default repository ([:material-docker: Docker Hub](https://hub.docker.com))

!!! info
    **How to pull the image of a specific distro (es. Alpine) without specifying the tag version?** (:warning: to be tested): get all the tags of a specific `image` in a list (you will need the JSON processor [jq](https://stedolan.github.io/jq/), just use `apt-get install jq`) and filtering them by distro with `grep`:
    ```bash
    wget -q https://registry.hub.docker.com/v1/repositories/postgres/tags -O - | jq -r '.[].name' | grep '\-alpine'
    ```
    Replace `postgres` with your image name

* `docker container ls -al`: list all the containers
* `docker container cp FILE CONTAINER_NAME:/`: it copies `FILE` in the root folder of the `CONTAINER_NAME`

* `docker run`: main command for running containers
* `docker run -p HOST_PORT:CONTAINER_PORT --name YOUR_CONTAINER_NAME -e ENVIRONMENT_VARIABLE=variable_value -d IMAGE_NAME`: it will run (and optionally pull, if the corresponding `IMAGE_NAME` hasn't been downloaded yet) a new container in the background (detached mode, or `-d`), naming it `YOUR_CONTAINER_NAME`, mapping the specified `CONTAINER_PORT` (handled in the container's virtual network) to the specified `HOST_PORT` and setting the specified `ENVIRONMENT_VARIABLE`

    > Example: `docker run --name postgres14 -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=secretpassword -d postgres:14-alpine`

!!! warning :warning: 
    The error **docker: Error response from daemon: driver failed programming external connectivity on endpoint ...: Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use** means that the specified local port (i.e. in the example, the bind `0.0.0.0:5432`) is already used by another process... Just change the host port :ok_hand:.

* `docker exec -it CONTAINER_NAME_OR_ID COMMAND [ARGS]`: it will run interactively (i.e. by opening a shell session, `-it`) the `COMMAND` with its `ARGS` in the `CONTAINER_NAME_OR_ID`

    > Example: `docker exec -it postgres14 psql -U root`

* `docker logs CONTAINER_NAME_OR_ID`: it shows the logs of the specified `CONTAINER_NAME_OR_ID`

## Quick ones

* Get the docker image ID by its name (`IMAGE-NAME`):
```bash
docker images --format="{{.Repository}} {{.ID}}" |      # Reformat the output of 'docker images'
grep "IMAGE-NAME" |         # Find your image
cut -d' ' -f2               # Cut the output and pick the ID
```

* [Remove all Exited containers](https://coderwall.com/p/zguz_w/docker-remove-all-exited-containers): it may occur that some containers with running processes are in the `Exited` status and therefore won't be deleted with the `docker container rm` command - or, the specific ID will be removed and immediately replaced with another one. Then just run:
```bash
sudo docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs sudo docker rm
```

* To avoid typing long bash commands, automate the most usual ones with a [Makefile](https://www.gnu.org/software/make/manual/make.html) (also a tutorial at [Makefiletutorial](https://makefiletutorial.com/)). The Makefile follows the syntax:
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