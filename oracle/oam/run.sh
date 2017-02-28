#!/bin/bash
# Runs the docker container and mounts the MW_HOME directory from the host mapping it to /u01/oracle
# If the mapping changes, ie, the mounted point in the container changes, the create_oam_domain.py
# file needs to be updated with the new mapping
# docker run --env-file ./env.list -v /u01/oracle:/u01/oracle -h docker.mycompany.com  -t -p 7001:7001 -p 7002:7002 -p 14100:14100 -p 14101:14101 -i oracle-iam/oam-r2ps3 
# docker run --env-file env.list -v /u01/oracle:/u01/oracle -td -p 7001:7001 -p 7002:7002 -p 14100:14100 -p 14101:14101 -i oracle-iam/oam-r2ps3
docker run --env-file ./env.list -h docker.mycompany.com  -t -p 7001:7001 -p 7002:7002 -p 14100:14100 -p 14101:14101 -i oracle-iam/oam-r2ps3
