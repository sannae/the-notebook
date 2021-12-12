# docker :material-docker:

??? Resources
    * [:material-docker: Docker docs](https://docs.docker.com/)! The starting point
    * [:material-youtube: Dev containers](https://www.youtube.com/playlist?list=PLj6YeMhvp2S5G_X6ZyMc8gfXPMFPg3O31), a playlist from the VS Code YouTube channel about containerized dev environments

## Architecture

* Container virtualization layers:
![container-virtualization-layers](https://docs.microsoft.com/en-us/learn/modules/intro-to-docker-containers/media/5-efficient-use-hardware.svg)

* Components of the Docker Engine:
    * **docker client**: a CLI-based application named `docker` to interact with the local or remote Docker server via the Docker REST API. 
    * **docker server** or **docker daemon**: a daemon named `dockerd`, responding to requests from the client via the Docker REST API and interacting with other daemons.
![components-of-docker-engine](https://docs.microsoft.com/en-us/learn/modules/intro-to-docker-containers/media/2-docker-architecture.svg)

* Container lifecycle:
![container-lifecycle](https://docs.microsoft.com/en-us/learn/modules/intro-to-docker-containers/media/4-docker-container-lifecycle.svg)

## Most used commands

### Processes

* `docker ps -a`: list of all containers and their statuses

### Images

* `docker images`: main command for managing images; by itself, it lists the available images
    * `docker images rm IMAGE_ID`: it removes the image with the specified ID
    * `docker images --filter "dangling=true"`: lists all dangling images
    * `docker images prune`: deletes all [:material-stack-overflow: dangling images](https://stackoverflow.com/a/45143234)
    * `docker images prune -a`: deletes all [:material-stack-overflow: dangling and unused images](https://stackoverflow.com/a/45143234)

* `docker pull IMAGE_NAME:TAG`: it downloads the image with the specified name (and the specified `TAG`, or `latest` if not specified) from the default repository ([:material-docker: Docker Hub](https://hub.docker.com))

> Example: `docker pull postgres:14.0-alpine` will download the official `postgres` image at its 14th version on Linux Alpine

!!! info
    **How to pull the image of a specific distro (es. Alpine) without specifying the tag version?** (:warning: to be tested): get all the tags of a specific `image` in a list (you will need the JSON processor [jq](https://stedolan.github.io/jq/), just use `apt-get install jq`) and filtering them by distro with `grep`:
    ```bash
    wget -q https://registry.hub.docker.com/v1/repositories/postgres/tags -O - | jq -r '.[].name' | grep '\-alpine'
    ```
    Replace `postgres` with your image name

### Containers

### Operate on containers

* `docker container`: main command for managing containers
    * `docker container ls -al`: it lists all the containers, even the stopped ones
    * `docker container rm CONTAINER_ID`: it removes the container with the specified ID
    * `docker container cp FILE CONTAINER_NAME:/`: it copies `FILE` in the root folder of the `CONTAINER_NAME`

### Run containers

* `docker run`: main command for running containers
    * `docker run --name YOUR_CONTAINER_NAME -e ENVIRONMENT_VARIABLE=variable_value -d IMAGE_NAME`: it will run (and optionally pull, if the corresponding `IMAGE_NAME` hasn't been downloaded yet) a new container in the background (detached mode, or `-d`), naming it `YOUR_CONTAINER_NAME` and setting the specified `ENVIRONMENT_VARIABLE`
    * `docker run -p HOST_PORT:CONTAINER_PORT`: it runs the specified container mapping the specified `CONTAINER_PORT` (handled in the container's virtual network) to the specified `HOST_PORT`

> Example: `docker run --name postgres14 -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=secretpassword -d postgres:14-alpine`

:warning: The error **docker: Error response from daemon: driver failed programming external connectivity on endpoint ...: Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use** means that the specified local port (i.e. in the example, the bind `0.0.0.0:5432`) is already used by another process... Just change the host port :ok_hand:.

### Execute commands on containers

* `docker exec`: main command for executing commands on a container
    * `docker exec -it CONTAINER_NAME_OR_ID COMMAND [ARGS]`: it will run interactively (i.e. by opening a shell session, `-it`) the `COMMAND` with its `ARGS` in the `CONTAINER_NAME_OR_ID`

> Example: `docker exec -it postgres14 psql -U root`

### View container logs

* `docker logs CONTAINER_NAME_OR_ID`: it shows the logs of the specified `CONTAINER_NAME_OR_ID`

## Quick ones

* [Remove all Exited containers](https://coderwall.com/p/zguz_w/docker-remove-all-exited-containers): it may occur that some containers with running processes are in the `Exited` status and therefore won't be deleted with the `docker container rm` command - or, the specific ID will be removed and immediately replaced with another one. Then just run:
```bash
sudo docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs sudo docker rm
```

* To take advantage of the ~20 free private repositories of Canister, configure the docker CLI to use it as the default registry with
```bash
docker login --username=yourcanisterID --password=yourpassword cloud.canister.io:5000
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
