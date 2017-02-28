FROM oracle-iam/jdk7_u79

MAINTAINER Paulo Albuquerque <paulogpafilho@gmail.com>

USER root

ENV WLS_PKG=wls1036_generic.jar \
    NODE_MANAGER_PROPERTIES=nodemanager.properties \
    PSU_PKG=p23743997_1036_Generic.zip \
    PSU_PATCH_ID=K25M \
    WL_HOME=${MIDDLEWARE_BASE}/Middleware/wlserver_10.3 \
    USER_MEM_ARGS="-Djava.security.egd=file:/dev/./urandomi -Dweblogic.security.SSL.enableJSSE=true"

COPY ${WLS_PKG} silent.xml ${PSU_PKG} ${NODE_MANAGER_PROPERTIES} ${MIDDLEWARE_BASE}/

RUN  mkdir ${MIDDLEWARE_BASE}/Middleware && \
     chown -R oracle:oinstall ${MIDDLEWARE_BASE}

USER oracle

RUN cd ${MIDDLEWARE_BASE} && \
    java -d64 -jar ${WLS_PKG} -mode=silent -silent=./silent.xml && \
    mkdir -p "${MIDDLEWARE_BASE}/Middleware/utils/bsu/cache_dir" && \
    unzip ${MIDDLEWARE_BASE}/${PSU_PKG} -d ${MIDDLEWARE_BASE}/Middleware/utils/bsu/cache_dir && \
    chmod 750 ${MIDDLEWARE_BASE}/Middleware/utils/bsu/*.jar && \
    sed -i 's/MEM_ARGS="-Xms256m -Xmx512m"/MEM_ARGS="-Xms1024m -Xmx1024m"/' ${MIDDLEWARE_BASE}/Middleware/utils/bsu/bsu.sh && \
    rm ${MIDDLEWARE_BASE}/silent.xml ${MIDDLEWARE_BASE}/$WLS_PKG ${MIDDLEWARE_BASE}/${PSU_PKG} && \
    cd ${MIDDLEWARE_BASE}/Middleware/utils/bsu && \
    ${MIDDLEWARE_BASE}/Middleware/utils/bsu/bsu.sh -install -patch_download_dir=${MIDDLEWARE_BASE}/Middleware/utils/bsu/cache_dir -patchlist=${PSU_PATCH_ID} -prod_dir=${WL_HOME} && \
    mv ${MIDDLEWARE_BASE}/${NODE_MANAGER_PROPERTIES} ${WL_HOME}/common/nodemanager && \
    rm ${MIDDLEWARE_BASE}/Middleware/utils/bsu/cache_dir/*.jar

WORKDIR /home/oracle

CMD "bash"
