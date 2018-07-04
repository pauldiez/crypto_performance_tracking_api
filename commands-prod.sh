#!/bin/bash

# set base vars
SERVER_HOST_IP=0.0.0.0
PROJECT_ROOT_DIR=$(pwd)
DOCKER_COMPOSE_FILE="${PROJECT_ROOT_DIR}/docker-compose-prod.yml"

# set vault vars
ENV_DIR="${PROJECT_ROOT_DIR}/env"
VAULT_PASSWORD=''
VAULT_DIR="${ENV_DIR}/vault"
VAULT_PASSWORD_FILE="${VAULT_DIR}/.vault_pass"
ANSIBLE_CONFIG_FILE="${VAULT_DIR}/ansible.cfg"

# env var files
PROD_ENV_VAR_FILE="${ENV_DIR}/production.env"
PROD_SECRET_ENV_VAR_FILE_ENCRYPTED="${ENV_DIR}/production-secrets-encrypted.env"
PROD_SECRET_ENV_VAR_FILE_DECRYPTED="${ENV_DIR}/production-secrets.env"


# import helper functions
source scripts/command_helper_methods.sh

# set command argument
COMMAND=$1
shift;

# read and set command line arguments
for i in "$@"
do
case ${i} in
	--vp=*|--vault-password=*)
        VAULT_PASSWORD="${i#*=}"
	    if [[ "${VAULT_PASSWORD}" = '' ]]; then
			echo "--vp|--vpassword (vault password) is required."
		    exit 1
		fi
		export_prod_env_vars
		decrypt_production_env_vars_file
	;;
    *)
        # everything else
    ;;
esac
done


case "${COMMAND}" in

'testing')
	testing_method
	echo ${REDIS_HOST}
	echo ${CELERY_TIMEZONE}
;;

'help'|'--help')
	echo "Command List:"
    echo "  "
    echo "  ** Some command will require --vp|--vpassword **"
    echo "  "
    echo "  install/mac"
    echo "  install/aws(|/ubuntu)"
    echo "  deploy                              [--vp|--vpassword, -r|--rebuild]"
    echo "  git/status"
    echo "  git/commit                          [-msg|--message]"
    echo "  git/commit/push                     [-msg|--message]"
    echo "  git/push                            [-f|--force]"
    echo "  git/pull"
    echo "  git/pull/force"
    echo "  up(|start|down)                     [-f|--composer-file, -d|daemon-mode, -s|composer-service]"
    echo "  restart                             [-f|--composer-file, -d|daemon-mode, -s|composer-service]"
    echo "  down(|shutdown)                     [-f|--composer-file]"
    echo "  tests"
    echo "  lint"
    echo "  db/list                             [-h|--host, --p|--port]"
    echo "  db/test                             [-h|--host, --p|--port]"
    echo "  db/(shell|connect)                  [-h|--host, --p|--port, -u|--user, -n|--name, --pw|--password]"
    echo "  db/create                           [-h|--host, --p|--port, -u|--user, -n|--name, --pw|--password]"
    echo "  db/drop(delete|remove)              [-h|--host, --p|--port, -u|--user, -n|--name, --pw|--password]"
    echo "  db/init                             [-f|--composer-file]"
    echo "  db/migrate                          [-f|--composer-file]"
    echo "  db/upgrade                          [-f|--composer-file]"
    echo "  db/downgrade                        [-f|--composer-file]"
    echo "  docker/containers(|/list)"
    echo "  docker/containers/running"
    echo "  docker/containers/stop"
    echo "  docker/containers/(remove|delete)"
    echo "  docker/images(|/list)"
    echo "  docker/images/(remove|delete)"
    echo "  docker/images/build                 [-f|--composer-file, -s|composer-service]"
    echo "  pip/install                         [-f|--composer-file, --pip-package"
    echo "  pip/install/reqs                    [-f|--composer-file]"
    echo "  redis/connect                       [-h|--host, --p|--port]"
    echo "  wipe                                [--vp|--vpassword,-a|--all, -f|--composer-file, -d|--db|--database, -m|--mf|--migration-folder, -i|--images, -c|--containers]"
    echo "  wipe/migration/folder"
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
	echo "Starting production servers in daemon mode..."
	docker-compose -f "${DOCKER_COMPOSE_FILE}" up ${DAEMON_MODE} ${COMPOSER_SERVICE}
;;

'restart')
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
	echo "Restarting production servers..."
	docker-compose -f "${DOCKER_COMPOSE_FILE}" down
	docker-compose -f "${DOCKER_COMPOSE_FILE}" up ${DAEMON_MODE} ${COMPOSER_SERVICE}
;;

'down'|'shutdown')
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done
	echo "Shutting down production servers..."
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
	for i in "$@"
	do
	case ${i} in
	    -f=*|--compose-file=*)
			DOCKER_COMPOSE_FILE="${i#*=}"
        ;;
	esac
	done
	echo "This is not tested, probably won't work"
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
	    -h=*|--host=*)
			HOST="${i#*=}"
        ;;
	esac
	done
	if [[ "${HOST}" = '' ]] ; then
		HOST=${SERVER_HOST_IP}
	fi
	migrate_database
;;

'db/upgrade')
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
	upgrade_database
;;

'db/downgrade')
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
	deploy_prod $@
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

if [[ "${VAULT_PASSWORD}" != '' ]]; then
	delete_decrypted_production_env_file
fi

exit 0