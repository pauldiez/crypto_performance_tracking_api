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




