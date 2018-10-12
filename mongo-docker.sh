#!/usr/bin/env bash
# Create a container from the mongo image,
#  run is as a daemon (-d), expose the port 27017 (-p),
#  set it to auto start (--restart)
#  and with mongo authentication (--auth)
# Image used is https://hub.docker.com/_/mongo/
docker pull mongo
docker run --name YOURCONTAINERNAME --restart=always -d -p 27017:27017 mongo mongod --auth

# Using the mongo "localhost exception" (https://docs.mongodb.org/v3.0/core/security-users/#localhost-exception)
# add a root user

# bash into the container
sudo docker exec -i -t YOURCONTAINERNAME bash

# connect to local mongo
mongo

# create the first admin user
use admin
db.createUser({user:"foouser",pwd:"foopwd",roles:[{role:"root",db:"admin"}]})

# exit the mongo shell
exit
# exit the container
exit

# now you can connect with the admin user (from any mongo client >=3 )
#  remember to use --authenticationDatabase "admin"
mongo -u "foouser" -p "foopwd" YOURHOSTIP --authenticationDatabase "admin"

# If hosted on Azure set the docker host keep alive timeout to less than 240 seconds
# that is the default keep alive time on Azure network infrastructure (Public Ip only)
# See also
# https://docs.mongodb.org/ecosystem/platforms/windows-azure/
# http://stackoverflow.com/questions/34373003/connection-timeout-to-mongodb-on-azure-vm