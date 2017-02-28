# Pull base image
# ---------------
FROM oracle-iam/iam-r2ps3

# Maintainer
# ----------
MAINTAINER Paulo Albuquerque <paulogpafilho@gmail.com>

# Environment variables required for this build (do not change)
# -------------------------------------------------------------
ENV USER_HOME=/home/oracle \
    CONFIG_SCRIPT=create_oam_domain.py \
    DOMAIN_SCRIPT=createOAMDomain.sh \
    RCU_PKG=ofm_rcu_linux_11.1.1.9.0_64_disk1_1of1.zip

EXPOSE 7001 7002 14100 14101 14150 14151 14180 14181

USER root

COPY ${CONFIG_SCRIPT} ${DOMAIN_SCRIPT} ${RCU_PKG} ${USER_HOME}/

RUN  unzip ${USER_HOME}/${RCU_PKG} -d ${MIDDLEWARE_BASE} && \
     rm ${USER_HOME}/${RCU_PKG} && \
     chown -R oracle:oinstall ${USER_HOME} ${CONFIG_BASE} ${MIDDLEWARE_BASE}

USER oracle

WORKDIR ${USER_HOME} 

CMD bash -C "/home/oracle/${DOMAIN_SCRIPT}";"bash"
