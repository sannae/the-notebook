# docker :material-docker:

* [:material-youtube: Dev containers](), a playlist from the VS Code YouTube channel about containerized dev environments

## Most used commands

* `docker ps -a`: list of containers and their statuses
  
* `docker images`: main command for managing images; by itself, it lists the available images
    * `docker images rm IMAGE_ID`: it removes the image with the specified ID
    * `docker images --filter "dangling=true"`: lists all dangling images
    * `docker images prune`: deletes all [:material-stack-overflow: dangling images](https://stackoverflow.com/a/45143234)
    * `docker images prune -a`: deletes all [:material-stack-overflow: dangling and unused images](https://stackoverflow.com/a/45143234)

* `docker container`: main command for managing containers
    * `docker container ls -al`: it lists all the containers, even the stopped ones
    * `docker container rm CONTAINER_ID`: it removes the container with the specified ID
    * `docker container cp FILE CONTAINER_NAME:/`: it copies `FILE` in the root folder of the `CONTAINER_NAME`

* `docker pull IMAGE_NAME:TAG`: it downloads the image with the specified name (and the specified `TAG`, or `latest` if not specified) from the default repository ([Docker Hub](https://hub.docker.com))

> Example: `docker pull postgres:14.0-alpine` will download the official `postgres` image at its 14th version on Linux Alpine

!!! question
    How to pull the image of a specific distro (es. Alpine) without specifying the tag version? (see optional answer below)

Maybe:
* Get all the tags of a specific `image` in a list (you will need the JSON processor [jq](https://stedolan.github.io/jq/), just use `apt-get install jq`) and filtering them by distro with `grep`:
```bash
wget -q https://registry.hub.docker.com/v1/repositories/postgres/tags -O - | jq -r '.[].name' | grep '-alpine'
```
Replace `postgres` with your image name

* `docker run`: main command for running containers
    * `docker run --name YOUR_CONTAINER_NAME -e ENVIRONMENT_VARIABLE=variable_value -d IMAGE_NAME`: it will run (and optionally pull, if the corresponding `IMAGE_NAME` hasn't been downloaded yet) a new container in the background (detached mode, or `-d`), naming it `YOUR_CONTAINER_NAME` and setting the specified `ENVIRONMENT_VARIABLE`
    * `docker run -p HOST_PORT:CONTAINER_PORT`: it runs the specified container mapping the specified `CONTAINER_PORT` (handled in the container's virtual network) to the specified `HOST_PORT`

> Example: `docker run --name postgres14 -p 5432:5432 -e POSTGRES_USER=root -e POSTGRES_PASSWORD=secretpassword -d postgres:14-alpine`

:warning: The error **docker: Error response from daemon: driver failed programming external connectivity on endpoint ...: Error starting userland proxy: listen tcp4 0.0.0.0:5432: bind: address already in use** means that the specified local port (i.e. in the example, the bind `0.0.0.0:5432`) is already used by another process... Just change the host port :ok_hand:.

* `docker exec`: main command for executing commands on a container
    * `docker exec -it CONTAINER_NAME_OR_ID COMMAND [ARGS]`: it will run interactively (i.e. by opening a shell session, `-it`) the `COMMAND` with its `ARGS` in the `CONTAINER_NAME_OR_ID`

> Example: `docker exec -it postgres14 psql -U root`

* `docker logs CONTAINER_NAME_OR_ID`: it shows the logs of the specified `CONTAINER_NAME_OR_ID`

* `docker container 


## Quick ones

* [Remove all Exited containers](https://coderwall.com/p/zguz_w/docker-remove-all-exited-containers):
```bash
sudo docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs sudo docker rm
```
