#!/bin/bash


# These are functions to help with repetitive tasks that are tied to the dev and production command/deployment scripts
# If you want to these helper function in other scripts,  you will need to examine the variables within each function
# to know which ones to populate before calling the helper functions


generate_vault()
{
	if [[ -z "${VAULT_PASSWORD}" ]] ; then
		echo "The VAULT_PASSWORD argument (vault password) for export_prod_env_vars() method is required."
        exit 1
	fi

	echo "generate vault..."

	echo  "make vault dir"
	mkdir -p "${VAULT_DIR}"

	echo "make password file"
	echo "${VAULT_PASSWORD}" > "${VAULT_PASSWORD_FILE}"

	echo "make ansible config"
	cat > "${ANSIBLE_CONFIG_FILE}" << EOF
[defaults]
vault_password_file = .vault_pass
EOF

}

enter_vault()
{
	echo "cd into vault dir - (${VAULT_DIR})"
	cd "${VAULT_DIR}"

}

exit_vault()
{
	echo "exit vault dir back to (${PROJECT_ROOT_DIR})"
	cd ${PROJECT_ROOT_DIR}

}
delete_vault()
{
	echo "deleting vault dir"
	rm -rf ${VAULT_DIR}

}
export_prod_env_vars()
{
	generate_vault
	enter_vault

	echo "extract vars from encrypted file - strip out comments - parse into a single line string - export decrypted vars"
	export $(ansible-vault view "${PROD_SECRET_ENV_VAR_FILE_ENCRYPTED}" | grep -v ^# | xargs)
	export $(cat "${PROD_ENV_VAR_FILE}" | grep -v ^# | xargs)

	echo "cd back into root dir"
	cd ${PROJECT_ROOT_DIR}

	exit_vault
	delete_vault
}

export_dev_env_vars()
{
	export $(cat "${DEV_ENV_VAR_FILE}" | grep -v ^# | xargs)
	export $(cat "${DEV_SECRET_ENV_VAR_FILE_DECRYPTED}" | grep -v ^# | xargs)
}

decrypt_production_env_vars_file()
{
	# We want to keep our production passwords and keys private, but yet at the same time
	# we also want to be able to commit and manage them in a repo.
	# So we have encrypted our sensitive data variables using ansible vault and then we decrypt them
	# from the vault via a vault password during server build process
	# reference - https://www.digitalocean.com/community/tutorials/how-to-use-vault-to-protect-sensitive-ansible-data-on-ubuntu-16-04#setting-the-ansible-vault-editor

	echo "decrypting secrets"
	generate_vault
	enter_vault

	# extract vars from encrypted file - strip out comments - parse into a single line string
	echo "decrypting production secret vars"
	ansible-vault decrypt "${PROD_SECRET_ENV_VAR_FILE_ENCRYPTED}"
	echo "making copy of decrypted files"
	cp "${PROD_SECRET_ENV_VAR_FILE_ENCRYPTED}" "${PROD_SECRET_ENV_VAR_FILE_DECRYPTED}"
	echo "re-encrypting production secret vars"
	ansible-vault encrypt "${PROD_SECRET_ENV_VAR_FILE_ENCRYPTED}"

	echo "cd back into root dir"
	cd ${PROJECT_ROOT_DIR}

	exit_vault
	delete_vault

}

delete_decrypted_production_env_file()
{
	echo "checking if decrypted production env file exists to delete"
	if [[ -e "${SECRET_ENV_VAR_FILE_DECRYPTED}" ]]
	then
		echo "delete decrypted production env file"
		rm "${SECRET_ENV_VAR_FILE_DECRYPTED}"
	fi
}

connect_to_cache()
{

	CACHE_HOST="${HOST}"
	CACHE_PORT="${PORT}"

	if [[ "${HOST}" = '' ]] ; then
	    HOST=${REDIS_HOST}
	fi

	if [[ "${PORT}" = '' ]] ; then
		PORT=${REDIS_PORT}
	fi

	redis-cli -c -h ${CACHE_HOST} -p ${CACHE_PORT}
}

is_cache_running()
{

	CACHE_HOST="${HOST}"
	CACHE_PORT="${PORT}"

	if [[ "${HOST}" = '' ]] ; then
	    CACHE_HOST=${POSTGRES_HOST}
	fi

	if [[ "${PORT}" = '' ]] ; then
		CACHE_PORT="${POSTGRES_PORT}"
	fi

	if [[ $(redis-cli -c -h "${CACHE_HOST}" -p "${CACHE_PORT}" ping | grep "PONG") = "PONG" ]]; then
		echo "true"
	else
		echo "false"
	fi

}
list_dbs()
{
	DB_HOST="${POSTGRES_HOST}"
	DB_PORT="${POSTGRES_PORT}"
	DB_NAME="${POSTGRES_DB}"
	DB_USER="${POSTGRES_USER}"
	DB_PASSWORD="${POSTGRES_PASSWORD}"

	if [[ "${HOST}" != '' ]] ; then
	    DB_HOST="${HOST}"
	fi
	if [[ "${PORT}" != '' ]] ; then
		DB_PORT="${PORT}"
	fi
	if [[ "${X_NAME}" != '' ]] ; then
	    DB_NAME="${X_NAME}"
	fi
	if [[ "${X_USER}" != '' ]] ; then
	    DB_USER="${X_USER}"
	fi
	if [[ "${PASSWORD}" != '' ]] ; then
		DB_PASSWORD="${PASSWORD}"
	fi

	echo "Connecting to database ${DB_NAME}"
	#echo "psql --host=${DB_HOST} --port=${DB_PORT} --username=${DB_USER} --dbname=${DB_NAME}"
	PGPASSWORD=${DB_PASSWORD} psql --host=${DB_HOST} --port=${DB_PORT} --username=${DB_USER} --list
}

wait_for_db_connection()
{
	DB_HOST="${POSTGRES_HOST}"
	DB_PORT="${POSTGRES_PORT}"
	DB_NAME="${POSTGRES_DB}"
	DB_USER="${POSTGRES_USER}"
	DB_PASSWORD="${POSTGRES_PASSWORD}"

	if [[ "${HOST}" != '' ]] ; then
	    DB_HOST="${HOST}"
	fi
	if [[ "${PORT}" != '' ]] ; then
		DB_PORT="${PORT}"
	fi
	if [[ "${X_NAME}" != '' ]] ; then
	    DB_NAME="${X_NAME}"
	fi
	if [[ "${X_USER}" != '' ]] ; then
	    DB_USER="${X_USER}"
	fi
	if [[ "${PASSWORD}" != '' ]] ; then
		DB_PASSWORD="${PASSWORD}"
	fi

	scripts/./wait-for.sh "${DB_HOST}:${DB_PORT}" -- echo "...Connected successfully make to db"

}


connect_to_db_cli()
{
	DB_HOST="${POSTGRES_HOST}"
	DB_PORT="${POSTGRES_PORT}"
	DB_NAME="${POSTGRES_DB}"
	DB_USER="${POSTGRES_USER}"
	DB_PASSWORD="${POSTGRES_PASSWORD}"

	if [[ "${HOST}" != '' ]] ; then
	    DB_HOST="${HOST}"
	fi
	if [[ "${PORT}" != '' ]] ; then
		DB_PORT="${PORT}"
	fi
	if [[ "${X_NAME}" != '' ]] ; then
	    DB_NAME="${X_NAME}"
	fi
	if [[ "${X_USER}" != '' ]] ; then
	    DB_USER="${X_USER}"
	fi
	if [[ "${PASSWORD}" != '' ]] ; then
		DB_PASSWORD="${PASSWORD}"
	fi

	echo "Connecting to database ${DB_NAME}"
	PGPASSWORD=${DB_PASSWORD} psql --host=${DB_HOST} --port=${DB_PORT} --username=${DB_USER} --dbname=${DB_NAME}
}

is_db_running()
{
	DB_HOST="${POSTGRES_HOST}"
	DB_PORT="${POSTGRES_PORT}"
	DB_USER="${POSTGRES_USER}"
	DB_PASSWORD="${POSTGRES_PASSWORD}"

	if [[ "${HOST}" != '' ]] ; then
	    DB_HOST="${HOST}"
	fi
	if [[ "${PORT}" != '' ]] ; then
		DB_PORT="${PORT}"
	fi
	if [[ "${X_USER}" != '' ]] ; then
	    DB_USER="${X_USER}"
	fi
	if [[ "${PASSWORD}" != '' ]] ; then
		DB_PASSWORD="${PASSWORD}"
	fi

	if [[ `PGPASSWORD="${DB_PASSWORD}" psql \
	    --host="${DB_HOST}" \
	    --port="${DB_PORT}" \
	    --username="${DB_USER}" \
	    --dbname=template1 \
	    -lqt | cut -d \| -f 1 | grep -w "template1" | xargs` = "template1" ]] ; then
	    echo "success"

	else
	    echo "fail"
	fi

}

create_db_if_not_exists()
{
	DB_HOST="${POSTGRES_HOST}"
	DB_PORT="${POSTGRES_PORT}"
	DB_NAME="${POSTGRES_DB}"
	DB_USER="${POSTGRES_USER}"
	DB_PASSWORD="${POSTGRES_PASSWORD}"

	if [[ "${HOST}" != '' ]] ; then
	    DB_HOST="${HOST}"
	fi
	if [[ "${PORT}" != '' ]] ; then
		DB_PORT="${PORT}"
	fi
	if [[ "${X_NAME}" != '' ]] ; then
	    DB_NAME="${X_NAME}"
	fi
	if [[ "${X_USER}" != '' ]] ; then
	    DB_USER="${X_USER}"
	fi
	if [[ "${PASSWORD}" != '' ]] ; then
		DB_PASSWORD="${PASSWORD}"
	fi

	
	echo "Checking if db ${DB_NAME} already exits"

	if [[ `PGPASSWORD=${DB_PASSWORD} psql \
	    --host="${DB_HOST}" \
	    --port="${DB_PORT}" \
	    --username="${DB_USER}" \
	    --dbname="${DB_NAME}" \
	    2>/dev/null \
	    -lqt | cut -d \| -f 1 | grep -w "${DB_NAME}" | xargs` != "${DB_NAME}" ]]; then

	    echo "Creating database ${DB_NAME}"
		PGPASSWORD="${DB_PASSWORD}" psql \
	    --host="${DB_HOST}" \
	    --port="${DB_PORT}" \
	    --username="${DB_USER}" \
	    --dbname=template1 \
		-c "CREATE DATABASE ${DB_NAME};"

	else
		echo "DB name already exits."
	fi
}

create_db_user()
{

	read -p "Enter a db username: " DB_USER_INPUT
	read -p "Enter a db password: " DB_PASSWORD_INPUT

	DB_HOST="${POSTGRES_HOST}"
	DB_PORT="${POSTGRES_PORT}"
	DB_NAME="${POSTGRES_DB}"
	DB_USER="${POSTGRES_USER}"
	DB_PASSWORD="${POSTGRES_PASSWORD}"

	if [[ "${HOST}" != '' ]] ; then
	    DB_HOST="${HOST}"
	fi
	if [[ "${PORT}" != '' ]] ; then
		DB_PORT="${PORT}"
	fi
	if [[ "${X_NAME}" != '' ]] ; then
	    DB_NAME="${X_NAME}"
	fi
	if [[ "${X_USER}" != '' ]] ; then
	    DB_USER="${X_USER}"
	fi
	if [[ "${PASSWORD}" != '' ]] ; then
		DB_PASSWORD="${PASSWORD}"
	fi

	echo "Creating db user ${DB_USER_INPUT} for db ${DB_NAME}..."

	PGPASSWORD="${DB_PASSWORD}" psql \
    --host="${DB_HOST}" \
    --port="${DB_PORT}" \
    --username="${DB_USER}" \
    --dbname="${DB_NAME}" \
	-c "CREATE USER ${DB_USER_INPUT} SUPERUSER PASSWORD '${DB_PASSWORD_INPUT}'; \
    GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER_INPUT};"

}

drop_db()
{
	DB_HOST="${POSTGRES_HOST}"
	DB_PORT="${POSTGRES_PORT}"
	DB_NAME="${POSTGRES_DB}"
	DB_USER="${POSTGRES_USER}"
	DB_PASSWORD="${POSTGRES_PASSWORD}"

	if [[ "${HOST}" != '' ]] ; then
	    DB_HOST="${HOST}"
	fi
	if [[ "${PORT}" != '' ]] ; then
		DB_PORT="${PORT}"
	fi
	if [[ "${X_NAME}" != '' ]] ; then
	    DB_NAME="${X_NAME}"
	fi
	if [[ "${X_USER}" != '' ]] ; then
	    DB_USER="${X_USER}"
	fi
	if [[ "${PASSWORD}" != '' ]] ; then
		DB_PASSWORD="${PASSWORD}"
	fi

	if [[ `PGPASSWORD="${DB_PASSWORD}" psql \
	    --host="${DB_HOST}" \
	    --port="${DB_PORT}" \
	    --username="${DB_USER}" \
	    --dbname="${DB_NAME}" \
	    -lqt | cut -d \| -f 1 | grep -w ${DB_NAME} | xargs` == ${DB_NAME} ]]; then

		tput setaf 1; read -p "Are you sure you want to delete db ${DB_NAME}? [yes|no] " INPUT
		tput setaf 15
		if [[ "${INPUT}" != "yes" ]] ; then
			echo "Cancelling command"
			exit 2
		fi

	    echo "Deleting database ${DB_NAME}"

		PGPASSWORD="${DB_PASSWORD}" \
		psql \
	    --host="${DB_HOST}" \
	    --port="${DB_PORT}" \
	    --username="${DB_USER}" \
	    --dbname=template1 \
		-c "DROP DATABASE ${DB_NAME};"
	else
		echo "No database to delete."
	fi

}

list_all_docker_containers()
{
	echo "Listing all docker containers"
	docker ps -a
}

list_running_docker_containers()
{
	echo "Listing only running docker containers"
	docker ps
}
delete_all_docker_containers()
{
	echo "Deleting all docker containers"
	docker rm -f $(docker ps -aq)
}

stop_all_docker_constainers()
{
	echo "Stoping all docker containers"
	docker stop $(docker ps -aq)
}

delete_all_docker_images()
{
	stop_all_docker_constainers
	#echo "Deleting all docker images (except for pycharm* images)"
	echo "Deleting all docker images"
	#docker rmi -f $(docker images -q | grep -v "$(docker images "pycharm*" -q)" | xargs)
	docker rmi -f $(docker images -q)
}

does_migration_folder_exist()
{
	[[ -d "${PROJECT_ROOT_DIR}${MIGRATION_DIR_PATH}" ]]
}

delete_migration_folder()
{
	echo "Deleting migration directory ${PROJECT_ROOT_DIR}${MIGRATION_DIR_PATH}"
	sudo rm -rf "${PROJECT_ROOT_DIR}${MIGRATION_DIR_PATH}"
}

list_all_docker_images()
{
	echo "Listing all docker images"
	docker images
}

build_docker_image()
{
	docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache ${COMPOSER_SERVICE}
}

install_pip_requirements()
{
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run --rm web pip install -r /app/backend/flask_app/requirements.txt --user --upgrade
}

install_pip_package()
{
	# set command arguments
	for i in "$@"
	do
	case ${i} in
	    --package=*|--pip-package=*)
		PIP_PACKAGE="${i#*=}"
        ;;
	esac
	done
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run --rm web pip install "${PIP_PACKAGE}" --user --upgrade
}

init_database()
{
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
	--rm web python /app/backend/flask_app/manage.py db init
}

migrate_database()
{
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
	--rm web python /app/backend/flask_app/manage.py db migrate
}

upgrade_database()
{
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
	--rm web python /app/backend/flask_app/manage.py db upgrade
}

downgrade_database()
{
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
	--rm web python /app/backend/flask_app/manage.py db downgrade
}


deploy_dev()
{
	echo "Deploying to development..."

	echo "Shutting down docker servers"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" down

	echo "Checking for rebuild docker images flag"
	if [[ "${REBUILD}" = true ]]; then
		echo "Re-building docker images"
		docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache
	fi

	echo "Checking if db image exists..."
	if [[ $(docker images -q postgres_db:v1 2> /dev/null) = "" ]]; then
		echo "Building db image.."
        docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache db
        echo "postgres_db:v1 built"
	else
		echo "db exists..."
	fi

	echo "Checking if cache image exists..."
	if [[ $(docker images -q redis_cache:v1 2> /dev/null) = "" ]]; then
		echo "Building cache image.."
        docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache cache
        echo "redis_cache:v1 built"
	else
		echo "cache exists..."
	fi

	echo "Checking if web_gateway (nginx) image exists..."
	if [[ $(docker images -q nginx:v1 2> /dev/null) = "" ]]; then
		echo "Building web_gateway (nginx) image.."
        docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache web_gateway
        echo "web_gateway:v1 built"
	else
		echo "web_gateway (nginx) exists..."
	fi

	echo "Checking if python_web image exists..."
	if [[ $(docker images -q python_web:v1 2> /dev/null) = "" ]]; then
		echo "Building python_web image.."
        docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache web
        echo "python_web:v1 built"
	else
		echo "python_web exists..."
	fi

	docker-compose -f "${DOCKER_COMPOSE_FILE}" up -d db

	sleep 10

	if ! is_db_running ; then
		echo " Can't connect to db. Script will now exit"
		exit 45
	fi

	echo "Setting up database..."
	echo "Creating db"

	create_db_if_not_exists

	echo "Performing a git pull request"
	git pull

	if ! does_migration_folder_exist ; then
		echo "No migration folder found - initializing migration table schemas"
		docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
		--rm web python /app/backend/flask_app/manage.py db init
	fi

	echo "Generate db migration changes"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
	--rm web python /app/backend/flask_app/manage.py db migrate

	echo "Apply migration changes"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
	--rm web python /app/backend/flask_app/manage.py db upgrade

	echo "Starting docker servers"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" up ${DAEMON_MODE}

}

deploy_prod()
{
	echo "Starting deploying to production..."

	echo "Shutting down docker servers"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" down

	echo "Checking for rebuild docker images flag"
	if [[ "${REBUILD}" = true ]]; then
		echo "Re-building docker images"
		docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache
	fi

	echo "Checking if web_gateway image exists..."
	if [[ $(docker images -q web_gateway:v1 2> /dev/null) == "" ]]; then
		echo "Building web_gateway image.."
        docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache web_gateway
		echo "web_gateway:v1 built"
	else
		echo "web_gateway:v1 already exists..."
	fi

	echo "Checking if python_web image exists..."
	if [[ $(docker images -q python_web:v1 2> /dev/null) == "" ]]; then
		echo "Building python_web image.."
        docker-compose -f "${DOCKER_COMPOSE_FILE}" build --no-cache web
		echo "python_web:v1 built"
	else
		echo "python_web:v1 already exists"
	fi

	echo "Setting up database..."
	echo "Creating db"

	if ! is_db_running ; then
		echo " Can't connect to db. Script will now exit"
		exit 45
	fi

	create_db_if_not_exists

	# pull in latest changes
	echo "Performing git pull force request..."
	git pull

	if ! does_migration_folder_exist ; then
		echo "No migration folder found - initializing migration table schemas"
		docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
		--rm web python /app/backend/flask_app/manage.py db init
	fi

	echo "Generate db migration changes"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
	--rm web python /app/backend/flask_app/manage.py db migrate

	echo "Apply migration changes"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" run \
	--rm web python /app/backend/flask_app/manage.py db upgrade

	echo "Starting docker servers"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" up ${DAEMON_MODE}

	delete_decrypted_production_env_file
}

wipe_migration_folder()
{
	delete_migration_folder
}

wipe()
{
	# warn user what is about to be done
	if [[ "${ARGUMENT_STRING}" != '' ]]  ; then
		tput setaf 1; read -p "Are you sure you want to delete ${ARGUMENT_STRING}? [yes|no] " INPUT
		tput setaf 15
		if [[ "${INPUT}" != "yes" ]] ; then
			echo "Cancelling command"
			exit 2
		fi
	else
		tput setaf 1
		echo "No wipe arguments specified to indicate what to remove. Cancelling wipe command..."
		tput setaf 15
		exit 9
	fi

	if [[ "${WIPE_DB}" = true ]] ; then
		drop_db
	fi

	echo "Shutting down dockers servers"
	docker-compose -f "${DOCKER_COMPOSE_FILE}" down

	if [[ "${WIPE_MIGRATION_FOLDER}" = true ]]; then
		delete_migration_folder
	fi

	if [[ "${WIPE_CONTAINERS}" = true ]] ; then
		delete_all_docker_containers
	fi

	if [[ "${WIPE_IMAGES}" = true ]] ; then
		delete_all_docker_images
	fi

}
