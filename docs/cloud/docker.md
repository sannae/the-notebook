# docker :material-docker:

??? Resources
    * [:material-docker: Docker docs](https://docs.docker.com/)! The starting point
    * [:material-youtube: Docker and Kubernetes complete tutorial](https://www.youtube.com/playlist?list=PL0hSJrxggIQoKLETBSmgbbvE4FO_eEgoB), a very detailed playlist from beginner to advanced level in both Docker and Kubernetes - it's also a [:fontawesome-solid-book: Udemy course](https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/), by the way
    * [:material-youtube: Dev containers](https://www.youtube.com/playlist?list=PLj6YeMhvp2S5G_X6ZyMc8gfXPMFPg3O31), a playlist from the VS Code YouTube channel about containerized dev environments
    * [:fontawesome-solid-euro-sign: Docker Mastery](https://www.udemy.com/course/docker-mastery/) Udemy course on Docker and Kubernetes, by a Docker Captain

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

## Basics

### [:material-docker: docker image](https://docs.docker.com/engine/reference/commandline/image/)

* `docker image ls`: list all images
* `docker image prune --all`: deletes all [:material-stack-overflow: dangling images](https://stackoverflow.com/a/45143234), check before deleting with `docker images --filter "dangling=true"`
* `docker image pull IMAGE_NAME:TAG`: it downloads the image with the specified name (and the specified `TAG`, or `latest` if not specified) from the default repository ([:material-docker: Docker Hub](https://hub.docker.com))

!!! info
    **How to pull the image of a specific distro (es. Alpine) without specifying the tag version?** (:warning: to be tested): get all the tags of a specific `image` in a list (you will need the JSON processor [jq](https://stedolan.github.io/jq/), just use `apt-get install jq`) and filtering them by distro with `grep`:
    ```bash
    wget -q https://registry.hub.docker.com/v1/repositories/postgres/tags -O - | jq -r '.[].name' | grep '\-alpine'
    ```
    Replace `postgres` with your image name

### [:material-docker: docker container](https://docs.docker.com/engine/reference/commandline/container/)

* `docker container ls -al`: list all the containers
* `docker container cp FILE CONTAINER_NAME:/`: it copies `FILE` in the root folder of the `CONTAINER_NAME`
* `docker container run --detach --publish HOST_PORT:CONTAINER_PORT --name YOUR_CONTAINER_NAME --env ENVIRONMENT_VARIABLE=variable_value IMAGE_NAME`: it will run (and optionally pull, if the corresponding `IMAGE_NAME` is not in the local cache) a new container in the background (detached mode, or `-d`), naming it `YOUR_CONTAINER_NAME`, mapping the specified `CONTAINER_PORT` (handled in the container's virtual network) to the specified `HOST_PORT` and setting the specified `ENVIRONMENT_VARIABLE`

> Example: `docker container run --name postgres14 --publish 5432:5432 --env POSTGRES_USER=root --env POSTGRES_PASSWORD=secretpassword --detach postgres:14-alpine`

> Learn on a running container: `docker run -d IMAGE_NAME ping google.com`, where the `ping google.com` command overrides the default image's startup command and leaves the container always running

!!! warning 
    :warning: The error **docker: Error response from daemon: driver failed programming external connectivity on endpoint ...: Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use** means that the specified local port (i.e. in the example, the bind `0.0.0.0:5432`) is already used by another process... Just change the host port :ok_hand:.

* `docker container exec --interactive --tty CONTAINER_NAME_OR_ID COMMAND [ARGS]`: it will run interactively (i.e. by opening a shell session, `-it`) the `COMMAND` with its `ARGS` in the `CONTAINER_NAME_OR_ID`

> Example: `docker container exec -it postgres14 psql -U root`

* `docker container stop CONTAINER_NAME_OR_ID`: it sends a `SIGTERM` signal to the primary process inside the container, letting it shut down on its own time and with its own clean-up procedure
* `docker container kill CONTAINER_NAME_OR_ID`: it sends a `SIGKILL` signal to the primary process inside the container, shutting it down _immediately_; it's automatically used by the Docker Server if the container's process does not respond to the `docker stop` command within 10 seconds. 

#### Troubleshoot a container

* `docker container logs CONTAINER_NAME_OR_ID`: log of the specified `CONTAINER_NAME_OR_ID`. This is the same output as running the container without the `--detach` flag.
* `docker container top CONTAINER_NAME_OR_ID`: list of processes running in the container

### Misc.

* `docker system prune`: it removes all stopped containers, all networks not used, all dangling images, all build cache

## `Dockerfile`

`FROM` is the base image

`WORKDIR` is the working directory on the container, set as reference to the next instructions

`COPY source dest` copies files from the relative path in `source` to the relative path in `dest`

`SHELL` changes the shell from the default one

`RUN` runs a command or a script in the selected shell

`CMD` contains the command to be executed once the container is started (`CMD`s are not committed into the built image, and the ones preceding the last one will be ignored)

## Quick tips

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

* To install an unpacked .NET Framework service using its executable on Docker, use the following Dockerfile:
```dockerfile
FROM mcr.microsoft.com/windows/servercore:ltsc2019
WORKDIR /app
COPY . "C:/app"
RUN ["C:/Windows/Microsoft.NET/Framework/v4.0.30319/InstallUtil.exe", "/i", "EXECUTABLE_NAME.exe"]
SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]
CMD c:\app\Wait-Service.ps1 -ServiceName 'SERVICE_NAME' -AllowServiceRestart
```
Where the `Wait-Service.ps1` script, meant to wait for a service to stop, is available [:material-github: here](https://github.com/MicrosoftDocs/Virtualization-Documentation/blob/main/windows-server-container-tools/Wait-Service/Wait-Service.ps1).
