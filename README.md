# The Gatherer
This repository aims to develop a data collection platform for the VirusRevolution CRC

It contains two subprojects: [Backend] and [Frontend]

## Container-driven development

For local development you can launch all parts (Frontend + Backend + Database) in a container. 

### Prerequisites

To launch the two containers (Code + DB), you need to install the following tools:

* [podman] - container runtime
* [yq] to read configuration from yaml files (should be available from you distributions package repository)
* [make] for orchestration (should be available from you distributions package repository) 

> We use a Makefile instead of a `compose.yaml` because with that, we can read configuration from config.yml, which is not possible (?) with compose alone.

## Provide configuration

Copy the file `config.yml.template to config.yml` and edit it to fulfill your needs.

## Launch DB and init

If you set up [config.yml] and [Backend/config.yml] properly, you can launch `make db_init`:

This will

* spin up the database container
* create the database configured on [Backend/config.yml]
* create a user with password as configured in [Backend/config.yml]
* grant access to the created database to the corresponding user

After that, you can launch the code locally by running `python server.py` in the Backend directory.

## Launch Backend in another container

* open a terminal at the project root
* issue `make`
    * this will create a network in podman, so the containers can communicate with each other
    * launch [mariadb] in a container
    * build an image containing a python runtime
    * launch a container with the python runtime and the code mounted into it 

[Backend]: Backend
[Backend/config.yml]: Backend/config.yml
[config.yml]: config.yml
[Frontend]: Frontend
[make]: https://www.gnu.org/software/make
[mariadb]: https://mariadb.org
[podman]: https://podman.io
[yq]: https://github.com/kislyuk/yq
