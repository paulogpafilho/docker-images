# Pull base image
# ---------------
FROM oracle-iam/wls1036_generic

# Maintainer
# ----------
MAINTAINER Paulo Albuquerque <paulogpafilho@gmail.com>

# Environment variables required for this build (do not change)
# -------------------------------------------------------------
ENV IAM_PKG_1=ofm_iam_generic_11.1.2.3.0_disk1_1of3.zip \
    IAM_PKG_2=ofm_iam_generic_11.1.2.3.0_disk1_2of3.zip \
    IAM_PKG_3=ofm_iam_generic_11.1.2.3.0_disk1_3of3.zip \
    INSTALL_FILE=iamsuite_install_only.rsp \
    ORA_INST_FILE=oraInst.loc \
    SCRIPT_FILE=installIAMHome.sh

USER root

ADD  ${IAM_PKG_1} ${IAM_PKG_2} ${IAM_PKG_3} ${INSTALL_FILE} ${ORA_INST_FILE} ${SCRIPT_FILE} ${MIDDLEWARE_BASE}/

RUN  cd ${MIDDLEWARE_BASE} && \
     unzip ${IAM_PKG_1} && \
     unzip ${IAM_PKG_2} && \
     unzip ${IAM_PKG_3} && \
     rm ${IAM_PKG_1} ${IAM_PKG_2} ${IAM_PKG_3} &&\
     chown -R oracle:oinstall ${MIDDLEWARE_BASE}

user oracle

RUN  cd ${MIDDLEWARE_BASE} && \
     chmod u+x ${SCRIPT_FILE} && \
     ${MIDDLEWARE_BASE}/${SCRIPT_FILE} && \
     rm ${SCRIPT_FILE} readme_idm_r2ps3.htm ${INSTALL_FILE} ${ORA_INST_FILE} && \
     rm -rf Disk1 Disk2 Disk3 logs

WORKDIR /home/oracle

CMD ["bash"]
