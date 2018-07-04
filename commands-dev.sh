#!/bin/bash

# set base vars
SERVER_HOST_IP=0.0.0.0
PROJECT_ROOT_DIR=$(pwd)
DOCKER_COMPOSE_FILE="${PROJECT_ROOT_DIR}/docker-compose.yml"

# env var files
ENV_DIR="${PROJECT_ROOT_DIR}/env"
DEV_ENV_VAR_FILE="${ENV_DIR}/development.env"
DEV_SECRET_ENV_VAR_FILE_DECRYPTED="${ENV_DIR}/development-secrets.env"

# import helper functions
source scripts/command_helper_methods.sh

# export dev env vars
export_dev_env_vars

# set command argument
COMMAND=$1
shift;

case "${COMMAND}" in

'testing')
	echo "  This is a play command for experimentations"
;;

'help'|'--help')
    echo "Command List:"
    echo "  "
    echo "  install/mac"
    echo "  install/aws(|/ubuntu)"
    echo "  deploy                              [-r|--rebuild]"
    echo "  git/status"
    echo "  git/commit                          [-m|-msg|--message]"
    echo "  git/commit/push                     [-m|-msg|--message]"
    echo "  git/push                            [-f|--force]"
    echo "  git/pull"
    echo "  git/pull/force"
    echo "  up(|start)                          [-f|--compose-file, -d|daemon-mode, -s|composer-service]"
    echo "  restart                             [-f|--compose-file, -d|daemon-mode, -s|composer-service]"
    echo "  down(|shutdown|stop)                [-f|--compose-file]"
    echo "  tests"
    echo "  lint"
    echo "  db/list                             [-h|--host, --p|--port]"
    echo "  db/test                             [-h|--host, --p|--port]"
    echo "  db/(shell|connect)                  [-h|--host, --p|--port, -u|--user, -n|--name, --pw|--password]"
    echo "  db/create                           [-h|--host, --p|--port, -u|--user, -n|--name, --pw|--password]"
    echo "  db/drop(delete|remove)              [-h|--host, --p|--port, -u|--user, -n|--name, --pw|--password]"
    echo "  db/init                             [-f|--compose-file]"
    echo "  db/migrate                          [-f|--compose-file]"
    echo "  db/upgrade                          [-f|--compose-file]"
    echo "  db/downgrade                        [-f|--compose-file]"
    echo "  docker/containers(|/list)"
    echo "  docker/containers/running"
    echo "  docker/containers/stop"
    echo "  docker/containers/(remove|delete)"
    echo "  docker/images(|/list)"
    echo "  docker/images/(remove|delete)"
    echo "  docker/images/build                 [-f|--compose-file, -s|composer-service]"
    echo "  pip/install                         [-f|--compose-file, --pip-package"
    echo "  pip/install/reqs                    [-f|--compose-file]"
    echo "  redis/connect                       [-h|--host, --p|--port]"
    echo "  wipe                                [-a|--all, -f|--compose-file, -d|--db|--database, -m|--mf|--migration-folder, -i|--images, -c|--containers]"
    echo "  wipe/migration/folder"
;;

'install/mac')
	scripts/./install-mac-osx.sh
;;

'install/aws'|'install/aws/ubuntu')
	scripts/./install-aws-ubuntu.sh
;;

'git/status')
	echo "Performing git status..."
	git status
;;

'git/commit')
	for i in "$@"
	do
	case ${i} in
	    -m=*|--msg=*|--message=*)
			COMMIT_MESSAGE="${i#*=}"
	    ;;
	esac
	done

	echo "Performing git commit"
	if [[ "${COMMIT_MESSAGE}" != "" ]] ; then
		git add . && git commit -m "${COMMIT_MESSAGE}"
	else
		git add . && git commit
	fi
;;

'git/commit/push')
	echo "Performing git commit and push..."
	for i in "$@"
	do
	case ${i} in
	    -m=*|--msg=*|--message=*)
			COMMIT_MESSAGE="${i#*=}"
	    ;;
	esac
	done
	if [[ "${COMMIT_MESSAGE}" != "" ]] ; then
		git add . && git commit -m "${COMMIT_MESSAGE}"  && git push
	else
		git add . && git commit  && git push
	fi
;;

'git/push')
	echo "Performing git push..."
	git push
;;

'git/pull')
	echo "Performing git pull"

	for i in "$@"
	do
	case ${i} in
	    -f|--force)
			FORCE=true
	    ;;
	esac
	done

	git pull
	if [[ "${FORCE}" = true ]] ; then
		echo " ....with force option"
		git fetch --all
        git reset --hard origin/master
	fi
;;

'up'|'start')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
        -s=*|--compose-service=*)
			DOCKER_COMPOSE_SERVICE="${i#*=}"
        ;;
        -d|--daemon-mode)
			DAEMON_MODE="-d"
        ;;
	esac
	done

	echo "Starting dev servers ${DOCKER_COMPOSE_SERVICE}"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" up ${DAEMON_MODE} ${DOCKER_COMPOSE_SERVICE}
;;

'restart')
	echo "Restarting dev servers..."
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
        -s=*|--compose-service=*)
			DOCKER_COMPOSE_SERVICE="${i#*=}"
        ;;
        -d|--daemon-mode)
			DAEMON_MODE="-d"
        ;;
	esac
	done

	docker-compose -f "${DOCKER_COMPOSE_FILE}" down
	docker-compose -f "${DOCKER_COMPOSE_FILE}" up ${DAEMON_MODE} ${DOCKER_COMPOSE_SERVICE}
;;

'down'|'shutdown'|'stop')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done

	docker-compose -f "${DOCKER_COMPOSE_FILE}" down
;;

'tests')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done

	echo "This is not tested, probably won't work"
	docker-compose -f docker-compose-test.yml run --rm test_app
;;

'lint')
	echo "This is not tested, probably won't work"
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done

	docker-compose -f docker-compose-test.yml run \
	--rm web bash -c "python -m flake8 /app/backend/flask_app/src /app/backend/flask_app/tests"
;;

'redis/connect')
	for i in "$@"
	do
	case ${i} in
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	connect_to_cache
;;

'db/test')
	for i in "$@"
	do
	case ${i} in
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi

	if [[ $(is_db_running) = 'success' ]] ; then
		echo " Connection successful."
		exit 45
	else
		echo " Can't connect to db. Script will now exit"
		exit 46
	fi
;;

'db/shell'|'db/connect')
	for i in "$@"
	do
	case ${i} in
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	connect_to_db_cli
;;

'db/list')
	for i in "$@"
	do
	case ${i} in
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	list_dbs
;;

'db/create')
	for i in "$@"
	do
	case ${i} in
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	create_db_if_not_exists
;;

'db/create/user')
	for i in "$@"
	do
	case ${i} in
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	create_db_user
;;

'db/drop'|'db/delete'|'db/remove')
	for i in "$@"
	do
	case ${i} in
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	drop_db
;;

'db/init')
	for i in "$@"
	do
	case ${i} in
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	init_database
;;

'db/migrate')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done
	migrate_database
;;

'db/upgrade')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done
	upgrade_database
;;

'db/downgrade')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done
	downgrade_database
;;

'docker/containers'|'docker/containers/list')
	list_all_docker_containers
;;

'docker/containers/running')
	list_running_docker_containers
;;

'docker/containers/stop')
	stop_all_docker_constainers
;;

'docker/containers/remove'|'docker/containers/delete')
	delete_all_docker_containers
;;

'docker/images'|'docker/images/list')
	list_all_docker_images
;;

'docker/images/remove'|'docker/images/delete')
	delete_all_docker_images
;;

'docker/images/build')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
        -s=*|--compose-service=*)
			DOCKER_COMPOSE_SERVICE="${i#*=}"
        ;;
	esac
	done
	build_docker_image
;;

'pip/install/reqs')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done
	install_pip_requirements
;;

'pip/install')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
         -p=*|--package=*)
			PIP_PACKAGE="${i#*=}"
        ;;
	esac
	done
	install_pip_package
;;

'wipe/migration/folder')

	#set vars
	WIPE_ALL=false

	# set arguments
	for i in "$@"
	do
	case ${i} in

		-h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done

	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	wipe_migration_folder $@
;;

'wipe')

	#set vars
	ARGUMENT_STRING=''
	# set arguments
	for i in "$@"
	do
	case ${i} in

		-h=*|--host=*)
			HOST="${i#*=}"
        ;;
	    -d|--db|--database)
	        WIPE_DB=true
	        ARGUMENT_STRING="${ARGUMENT_STRING} DATABASE,"
	    ;;
	    -i|--images)
	        WIPE_IMAGES=true
	        ARGUMENT_STRING="${ARGUMENT_STRING} IMAGES,"
	    ;;
	    -c|--containers)
	        WIPE_CONTAINERS=true
	        ARGUMENT_STRING="${ARGUMENT_STRING} CONTAINERS,"
	    ;;
	    -a|--all)
	        WIPE_DB=true
	        WIPE_CONTAINERS=true
	        WIPE_IMAGES=true
			ARGUMENT_STRING="EVERYTHING (database, images, containers)"
	    ;;
	esac
	done

	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	wipe $@
;;
'deploy')
	for i in "$@"
	do
	case ${i} in
		-f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
        -r|--rebuild)
	        REBUILD=true
	    ;;
	    -d|--daemon-mode)
			DAEMON_MODE="-d"
        ;;
        -h=*|--host=*)
			HOST="${i#*=}"
	    ;;
	    -p=*|--port=*)
			PORT="${i#*=}"
	    ;;
	    --pw=*|--password=*)
			PASSWORD="${i#*=}"
	    ;;
	    -n=*|--name=*)
			X_NAME="${i#*=}"
	    ;;
	    -u=*|--user=*)
			X_USER="${i#*=}"
	    ;;
	esac
	done

	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	deploy_dev $@
;;

*)
	# everything else
	echo "  "
	echo "  That command doesn't exists."
	echo "  Script is now exiting..."
	echo "  "
	exit 10
;;
esac

exit 0