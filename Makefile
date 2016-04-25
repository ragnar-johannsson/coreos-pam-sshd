NAME=ragnarb/coreos-pam-sshd
VERSION=0.1

.PHONY: container
container:
	docker build --tag ${NAME} ${CURDIR}
	docker tag ${NAME}:latest ${NAME}:${VERSION}

.PHONY: cloud-config
cloud-config:
	./gen-cloud-config.py

.PHONY: clean
clean:
	-docker rmi --force ${NAME}:latest
	-docker rmi --force ${NAME}:${VERSION}


