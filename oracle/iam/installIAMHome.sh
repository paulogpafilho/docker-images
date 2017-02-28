#!/bin/bash
export OUT_FILE=${MIDDLEWARE_BASE}/iamInstall.log
export FINISHED_PATTERN="Oracle IDM Suite completed successfully"
export ERROR_PATTERN="Internal Error"

function install_iam_home() {
    printf "Installing IAM Home...\n"
    ${MIDDLEWARE_BASE}/Disk1/install/linux64/runInstaller JVM_OPTIONS=" -mx512m -XX:MaxPermSize=512m " -jreLoc ${MIDDLEWARE_BASE}/jdk1.7.0_79 -invPtrLoc ${MIDDLEWARE_BASE}/oraInst.loc -silent -response ${MIDDLEWARE_BASE}/iamsuite_install_only.rsp -J-Doracle.installer.appendjre=false >| ${OUT_FILE} 2>&1

    timeout --signal=SIGTERM 600 tail -f ${OUT_FILE} | while read LOGLINE
    do
        printf "%s\n" "${LOGLINE}"
        if [[ "${LOGLINE}" == *"${FINISHED_PATTERN}"* ]]; then
            printf "\nInstallation Done\n"
            pkill -SIGTERM -P $$ timeout
            break
        elif [[ "${LOGLINE}" == *"${ERROR_PATTERN}"* ]]; then
            printf "\nError installing IAM Home\n"
            pkill -SIGKILL -P $$ timeout
            break
        fi
    done

    if [ $? -eq 1 ]; then
        printf "\nFailed to install IAM Home\n"
        exit 1
    else
        printf "\nIAM Home Installation done.\n"
        exit 0
    fi
    rm ${OUT_FILE}
}
install_iam_home
