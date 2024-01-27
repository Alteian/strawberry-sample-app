#!/bin/bash

if [ -z "$2" ]; then
    echo "Error: Provide environment name as the second argument (local, dev, prod)"
    exit 1
fi

environment="$2"

case "$1" in
    "docker_build")
        echo "Building docker image"
        docker-compose -f dockerfiles/docker-compose.$environment.yml build
        ;;
    "docker_run")
        echo "Running docker image"
        docker-compose -f dockerfiles/docker-compose.$environment.yml up
        ;;
    "docker_stop")
        echo "Stopping docker image"
        docker-compose -f dockerfiles/docker-compose.$environment.yml down
        ;;
    "docker_fresh_start")
        echo "Running fresh start"
        cp src/settings/envs/.local.sample src/settings/envs/.local
        docker-compose -f dockerfiles/docker-compose.$environment.yml up --build -d
        docker-compose -f dockerfiles/docker-compose.$environment.yml exec web python3 manage.py migrate
        docker-compose -f dockerfiles/docker-compose.$environment.yml exec web python3 manage.py dummy_product_data
        docker-compose -f dockerfiles/docker-compose.$environment.yml exec web python3 manage.py collectstatic --noinput
        ;;
    *)
        echo "Error: Provide valid argument (docker_build, docker_run, docker_stop, docker_fresh_start)"
        exit 1
        ;;
esac
