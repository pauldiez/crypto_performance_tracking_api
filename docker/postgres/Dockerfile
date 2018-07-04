FROM postgres:alpine

LABEL maintainer="some.email@gmail.com"

### DOCS ###

#Database Configuration

# There are many ways to set PostgreSQL server configuration. For information on what is available to configure, see the postgresql.org docs for the specific version of PostgreSQL that you are running. Here are a few options for setting configuration:

# Use a custom config file. Create a config file and get it into the container. If you need a starting place for your config file you can use the sample provided by PostgreSQL which is available in the container at /usr/share/postgresql/postgresql.conf.sample.

# Important note: you must set listen_addresses = '*'so that other containers will be able to access postgres.
# get the default config
#$ docker run -i --rm postgres cat /usr/share/postgresql/postgresql.conf.sample > my-postgres.conf

# customize the config

#  run postgres with custom config
# docker run -d --name some-postgres -v "$PWD/my-postgres.conf":/etc/postgresql/postgresql.conf postgres -c 'config_file=/etc/postgresql/postgresql.conf'
# Set options directly on the run line. The entrypoint script is made so that any options passed to the docker command will be passed along to the postgres server daemon. From the docs we see that any option available in a .conf file can be set via -c.

# docker run -d --name some-postgres postgres -c 'shared_buffers=256MB' -c 'max_connections=200'
