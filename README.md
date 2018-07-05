# About This App

**This project creates the ability to:**

* Pull in live Crypto Currency data from 3rd party data sources (scheduled twice daily)
* Store the live data into a database
* Query and summarize historical data by date via an API endpoints
* Provide a minimum level of authorization on api endpoints, and 
* Ability to deploy a dev environment locally and on a production environment remotely.

**Technology stack used:**

* DevOps development: Though dev-ops is not my strong suit when it comes to software development I utilized:
    * Docker and Docker Compose to implement my servers along with writing Bash scripts to manage them 
	* Used NGINX as a reverse proxy
	* WSGI python server, 
	* Postgres for storing persistent data
	* Redis for caching, and
	* Ansible Vault to secure and encrypt sensitive environment variables (passwords, keys etc..) from the public but still allow the environment variables to be under version control.

* Python development: 
	* Used Flask-RESTful to develop the project
	* Implement Celery to schedule daily data mining tasks and fire off background queue processes. 
	* Used Marshmallow for data validation and
	* SQLAlchemy as an ORM.

Unfortunately this project doesn't showcase Unit Test Cases nor a testing harness/environment.

#Install app instructions

Download the crypto_api_public repo and cd into the repo directory

```bash
$ git clone https://pdiez@bitbucket.org/pdiez/crypto_api_public.git project
$ cd project
```



**Development installation instructions** 

Then run the following commands to install app dependencies for Mac and deploy app (docker, docker-composer, make, etc.):

```bash
$ chmod +x scripts/install-mac-osx.sh
$ ./command-dev.sh install/mac
$ ./command-dev.sh deploy
```

Now visit <http://[localhost-ip:8080]>


**Production installation instructions** 

Then run the install script to install App dependencies for AWS and deploy app (docker, docker-composer, make, etc.):

```bash
$ chmod +x scripts/install-aws-ubuntu.sh
$ ./command-prod.sh install/aws
$ ./command-dev.sh deploy

```

Now visit <http://[insert-aws-public-ip]>




