#!/bin/bash

export ADMIN_SERVER_OUT=${USER_HOME}/AdminServer.out
export NODE_MANAGER_OUT=${USER_HOME}/NodeManager.out
export AS_STARTED_PATTERN="<Server started in RUNNING mode>"
export NM_STARTED_PATTERN="Plain socket listener started on port 5556"

function removeRCUBinaries() {
    rm -rf ${RCU_HOME}
}

function drop_schemas() {
    printf "Dropping database schemas...\n"
    ${RCU_HOME}/bin/rcu -silent -dropRepository -databaseType ${DATABASE_TYPE} -connectString ${DATABASE_HOST}:${DATABASE_PORT}:${DATABASE_SERVICE} -dbUser ${DATABASE_USER} -dbRole ${DATABASE_ROLE} -schemaPrefix ${DATABASE_SCHEMA_PREFIX} -component OPSS -component IAU -component MDS -component OAM -component OMSM -f <<EOF
${DATABASE_PASS}
${DATABASE_OPSS_PASS}
${DATABASE_IAU_PASS}
${DATABASE_IAU_PASS}
${DATABASE_OAM_PASS}
${DATABASE_OMSM_PASS}
EOF
}

function create_schemas() {
    printf "Creating database schemas...\n"
    ${RCU_HOME}/bin/rcu -silent -createRepository -databaseType ${DATABASE_TYPE} -connectString ${DATABASE_HOST}:${DATABASE_PORT}:${DATABASE_SERVICE} -dbUser ${DATABASE_USER} -dbRole ${DATABASE_ROLE} -schemaPrefix ${DATABASE_SCHEMA_PREFIX} -component OPSS -component IAU -component MDS -component OAM -component OMSM -f <<EOF
${DATABASE_PASS}
${DATABASE_OPSS_PASS}
${DATABASE_IAU_PASS}
${DATABASE_IAU_PASS}
${DATABASE_OAM_PASS}
${DATABASE_OMSM_PASS}
EOF
    if [ $? -eq 1 ]; then
        printf "\nFailed to create database schemas\n"
	exit 1
    fi
}

function start_node_manager() {
    printf "\nStarting NodeManager...\n"
    nohup ${MW_HOME}/wlserver_10.3/server/bin/startNodeManager.sh >| ${NODE_MANAGER_OUT} 2>&1 &
    timeout --signal=SIGKILL 30 tail -f ${NODE_MANAGER_OUT} | while read LOGLINE
    do
        printf "%s\n" "${LOGLINE}"
        if [[ "${LOGLINE}" == *"${NM_STARTED_PATTERN}"* ]]; then
            printf "\nNodeManager Started\n"
            pkill -SIGKILL -P $$ timeout
            break
        fi
    done
}


function start_admin_server() {
    printf "Starting AdminServer...\n"
    
    nohup ${BASE_PATH}/domains/${DOMAIN_NAME}/startWebLogic.sh >| ${ADMIN_SERVER_OUT} 2>&1 &

    timeout --signal=SIGKILL 420 tail -f ${ADMIN_SERVER_OUT} | while read LOGLINE
    do
        printf "."
        if [[ "${LOGLINE}" == *"${AS_STARTED_PATTERN}"* ]]; then
            printf "\nAdminServer Started\n"
            pkill -SIGKILL -P $$ timeout
            break
        fi 
    done

    if [ $? -eq 1 ]; then
        printf "\nFailed to start AdminServer\n"
        exit 1
    fi


    STARTED=`grep -w "${PATTERN}" ${ADMIN_SERVER_OUT}`

    if [ "${STARTED}" == "" ]; then
        printf "AdminServer might have not started, check the output at ${OUT_FILE}"
    fi
}

function configure_security_store() {
    printf "Configuring Security Store...\n"

    ${MW_HOME}/oracle_common/common/bin/wlst.sh -skipWLSModuleScanning ${MW_HOME}/IAM/common/tools/configureSecurityStore.py -d /u02/oracle/domains/OAMDomain -c IAM -p ${DATABASE_OPSS_PASS} -m create

    if [ $? -eq 1 ]; then
        printf "\nFailed to configure Security Store\n"
        exit 1
    fi
}

function create_domain() {

    printf "Creating OAM Domain...\n"

    ${MW_HOME}/IAM/common/bin/wlst.sh -skipWLSModuleScanning ${USER_HOME}/create_oam_domain.py
    
    if [ $? -eq 1 ]; then
        printf "\nFailed to create domain\n"
        exit 1
    fi
}

function check_installation() {
    if [ ! -d "${BASE_PATH}/domains/${DOMAIN_NAME}" ]; then
        printf "Domain not created, starting domain creation...\n"
        drop_schemas
        create_schemas
        create_domain
        configure_security_store
        start_admin_server
    else
        printf "Domain already configured, skipping domain creation...\n"
        start_admin_server
    fi
}

start_node_manager
check_installation
