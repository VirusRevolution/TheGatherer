PROJECT="the_gatherer"
DB_ROOT_PASS=$$(yq -r .local_database.root_pass config.yml)
STORAGE=$$(yq -r .storage config.yml)

default: development_environment

# run a development environment, consisting of a databse container and the software in a container
development_environment: network local_database local_webservice

network:
	podman network create ${PROJECT}_net

# launch the database for local development in a container
local_database: local_storage
	podman run --name ${PROJECT}_db \
	     --replace \
		 --env MARIADB_ROOT_PASSWORD=${DB_ROOT_PASS} \
		 --volume ${STORAGE}/mariadb:/var/lib/mysql:Z \
		 --network ${PROJECT}_net \
		 -p 127.0.0.1:3306:3306 \
		 --detach docker.io/mariadb:latest

# build a container image to run the code in
image:
	podman build -t ${PROJECT} .

# run the code in a container image
local_webservice: image
	podman run --name ${PROJECT}_web \
	  --replace \
	  --volume $$(pwd):/opt/crc \
	  --network ${PROJECT}_net \
	  -p 8000:8000 \
	  -ti ${PROJECT}

# make sure the storage directory exists
local_storage:
	mkdir -p ${STORAGE}/mariadb

clean:
	podman rm -f ${PROJECT}_db ${PROJECT}_web