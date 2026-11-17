default: devel

build: devel-image
	podman run --name svelte-build \
		--rm \
		-v $$(dirname $$(pwd))://frontend \
		-ti svelte /opt/svelte-build

devel-image:
	podman build \
		--tag svelte \
		--file Dockerfile.svelte .

devel: devel-image
	-podman rm -f svelte
	podman run --name svelte \
		-v $$(dirname $$(pwd)):/frontend \
		-p 127.0.0.1:5173:5173 \
		-ti svelte /opt/svelte-init

release-image: build
	podman build \
		--tag frontend \
		--file Dockerfile.release ..

PORT = 8080

server:
	-podman rm -f vjdb-frontend-nginx
	podman run --name vjdb-frontend-nginx \
		-v $$(dirname $$(pwd))/dist:/frontend \
		-v ./config/default.conf:/etc/nginx/conf.d/default.conf:ro \
		-p ${PORT}:80 \
		docker.io/library/nginx:latest
