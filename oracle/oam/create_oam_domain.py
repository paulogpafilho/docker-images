import os
from shutil import copyfile
#-----------------------------------------------------------------------------
# Constants - Don't change
#-----------------------------------------------------------------------------
# Base path - where domain artifacts will be created
base_path = os.environ.get('BASE_PATH', '/u02/oracle')
domain_path  = base_path + '/domains'
applications_path =  base_path + '/applications'
# Domain name
domain_name  = 'OAMDomain'
# Machine name
machine_name = 'machine1'
# AdminServer ip adress
admin_server_ip = ''
# AdminServer port
admin_server_port = 7001
# AdminServer SSL port
admin_server_ssl_port = 7002
# OAM server ip address
oam_server_ip = ''
# OAM server port
oam_server_port = 14100
# OAM server SSL port
oam_server_ssl_port = 14101
# OMS server ip address
oms_server_ip = ''
# OMS server port
oms_server_port = 14180
# OMS server SSL port
oms_server_ssl_port = 14181
# OPM server ip address
opm_server_ip = ''
# OPM server port
opm_server_port = 14150
# OPM server SSL port
opm_server_ssl_port = 14151
#-----------------------------------------------------------------------------
# Variables - Editable
#-----------------------------------------------------------------------------
# Middleware Home - the path to the Middleware home where WLS and IAM 
# products are installed. This path should match the path of mounted host
# directory when running the container. See run.sh.
mw_home = os.environ.get('MW_HOME', '/tmp/Middleware')
# IAM home - Directory where IAM product is installed
iam_home = os.environ.get('IAM_HOME', '/tmp/Middleware/IAM')
# WLS admin user password
admin_pass   = os.environ.get('ADMIN_PASSWORD', 'ChangeMe')
# Node manager IP address
nodemanager_ip = os.environ.get('NODEMANAGER_IP', '')
# Node manager port
nodemanager_port = int(os.environ.get('NODEMANAGER_PORT', '5556'))
# Node manager password - The password of the node manager running
# in the host machine
#nodemanager_pass = os.environ.get('NODEMANAGER_PASSWORD', 'ChangeMe')
# Node manager user - The user of the node manager running
# in the host machine
#nodemanager_user = os.environ.get('NODEMANAGER_USER', 'weblogic')
# Database host
database_host = os.environ.get('DATABASE_HOST', 'localhost')
# Database port
database_port = os.environ.get('DATABASE_PORT', '1521')
# Database service
database_service = os.environ.get('DATABASE_SERVICE', 'orcl')
# OPSS schema user
database_opss_schema = os.environ.get('DATABASE_OPSS_SCHEMA', 'DEV_OPSS')
# OPSS schema password
database_opss_pass = os.environ.get('DATABASE_OPSS_PASS', 'ChangeMe')
# MDS schema user
database_mds_schema = os.environ.get('DATABASE_MDS_SCHEMA', 'DEV_MDS')
# MDS schema password
database_mds_pass = os.environ.get('DATABASE_MDS_PASS', 'ChangeMe')
# OAM schema user
database_oam_schema = os.environ.get('DATABASE_OAM_SCHEMA', 'DEV_OAM')
# OAM schema password
database_oam_pass = os.environ.get('DATABASE_OAM_PASS', 'ChangeMe')
# OMSM schema user
database_omsm_schema = os.environ.get('DATABASE_OMSM_SCHEMA', 'DEV_OMSM')
# OMSM schema password
database_omsm_pass = os.environ.get('DATABASE_OMSM_PASS', 'ChangeMe')
#-------------------------------------------------------------
# Configure a new OAM domain
#-------------------------------------------------------------
def configureOAMDomain():
    #print 'Configuring OAM domain'
    #print 'DATABASE_OPSS_SCHEMA: ' + database_opss_schema
    #print 'DATABASE_MDS_SCHEMA: '  + database_mds_schema
    #print 'DATABASE_OAM_SCHEMA: '  + database_oam_schema
    #print 'DATABASE_OMSM_SCHEMA: ' + database_omsm_schema
    #-------------------------------------------------------------
    hideDisplay()
    hideDumpStack('true')
    #-------------------------------------------------------------
    # Read WLS Template
    print 'Reading templates...'
    readTemplate(mw_home + '/wlserver_10.3/common/templates/domains/wls.jar')
    # Adds OAM Template
    addTemplate(iam_home + '/common/templates/applications/oracle.oam_ds_mobile_11.1.2.3_template.jar')
    #-------------------------------------------------------------
    # Get Encryption service
    print 'Getting Encryption Service...'
    if not os.path.exists(domain_path + '/' + domain_name + '/security'):
        os.makedirs(domain_path + '/' + domain_name + '/security')
    encryptSrv = weblogic.security.internal.SerializedSystemIni.getEncryptionService(domain_path + '/' + domain_name)
    ces = weblogic.security.internal.encryption.ClearOrEncryptedService(encryptSrv)
    #-------------------------------------------------------------
    # Create Machine and sets NM Properties
    print 'Setting Node Manager properties...'
    cd('/')
    create(machine_name, 'Machine') 
    cd('Machine/' + machine_name)
    create(machine_name, 'NodeManager')
    cd('NodeManager/' + machine_name)
    set('ListenAddress', nodemanager_ip)
    set('ListenPort', nodemanager_port)
    set('NMType', 'Plain')
    #-------------------------------------------------------------
    # Create Clusters
    print 'Creating clusters...'
    cd('/')
    create('oam_cluster', 'Cluster')
    create('oms_cluster', 'Cluster')
    create('opm_cluster', 'Cluster')
    #-------------------------------------------------------------
    # Create Embedded LDAP
    print 'Setting Embedded LDAP...'
    cd('/')
    create(domain_name, 'EmbeddedLDAP')
    cd('EmbeddedLDAP/' + domain_name)
    set('CredentialEncrypted', ces.encrypt(admin_pass))
    #-------------------------------------------------------------
    # Set Apps deployment targets
    print 'Setting application deployment...'
    # DMS
    cd('/AppDeployment/DMS Application#11.1.1.1.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')
    # WSIL-WL
    cd('/AppDeployment/wsil-wls')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')
    # WSM-PM
    cd('/AppDeployment/wsm-pm')
    set('Target', 'oms_cluster')
    # EM
    cd('/AppDeployment/em')
    set('SourcePath', applications_path + '/' + domain_name + '/em.ear')
    set('InstallDir', applications_path + '/' + domain_name)
    set('StagingMode', 'stage')
    # OAM server
    cd('/AppDeployment/oam_server#11.1.2.0.0')
    set('Target', 'oam_cluster')
    # OAMSSO
    cd('/AppDeployment/oamsso_logout#11.1.2.0.0')
    set('Target', 'AdminServer,oam_cluster,opm_cluster')
    # OMSM
    cd('/AppDeployment/omsm#11.1.2.3.0')
    set('Target', 'oms_cluster')
    # OAM policy Manager
    cd('/AppDeployment/oam_policy_mgr#11.1.2.0.0')
    set('Target', 'opm_cluster')
    #-------------------------------------------------------------
    # SET LIBRARY TARGETS
    print 'Setting libraries deployment...'
    cd('/Library/oracle.bi.adf.model.slib#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.bi.adf.view.slib#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.bi.adf.webcenter.slib#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.wsm.seedpolicies#11.1.1@11.1.1')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.jsp.next#11.1.1@11.1.1')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.dconfig-infra#11@11.1.1.1.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/orai18n-adf#11@11.1.1.1.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.adf.dconfigbeans#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.pwdgen#11.1.1@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.jrf.system.filter')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/adf.oracle.domain#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/adf.oracle.businesseditor#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.adf.management#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/adf.oracle.domain.webapp#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/jsf#1.2@1.2.9.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/jstl#1.2@1.2.0.1')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/UIX#11@11.1.1.1.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/ohw-rcf#5@5.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/ohw-uix#5@5.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.adf.desktopintegration.model#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.adf.desktopintegration#1.0@11.1.1.2.0')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.bi.jbips#11.1.1@0.1')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.bi.composer#11.1.1@0.1')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.omsas.ui.core#1.0@11.1.1.0')
    set('Target', 'opm_cluster')

    cd('/Library/oracle.webcenter.skin#11.1.1@11.1.1')
    set('Target', 'AdminServer,opm_cluster')

    cd('/Library/oracle.sdp.client#11.1.1@11.1.1')
    set('Target', 'AdminServer,oam_cluster,oms_cluster,opm_cluster')

    cd('/Library/oracle.webcenter.composer#11.1.1@11.1.1')
    set('Target', 'AdminServer,oam_cluster,opm_cluster')

    cd('/Library/oracle.idm.common.model#11.1.1@11.1.1')
    set('Target', 'AdminServer,oam_cluster,opm_cluster')

    cd('/Library/oracle.idm.uishell#11.1.1@11.1.1')
    set('Target', 'AdminServer,oam_cluster,opm_cluster')

    cd('/Library/oracle.idm.ipf#11.1.2@11.1.2')
    set('Target', 'AdminServer,oam_cluster,opm_cluster')

    cd('/Library/oracle.idm.ids.config.ui#11.1.2@11.1.2')
    set('Target', 'AdminServer,oms_cluster,opm_cluster')

    cd('/Library/oracle.oaam.libs#11.1.2.0.0@11.1.2.0.0')
    set('Target', 'oam_cluster,opm_cluster')

    cd('/Library/oracle.idm.msm.ui.library#11.1.2@11.1.2')
    set('Target', 'oms_cluster,opm_cluster')

    cd('/Library/jax-rs#1.1@1.9')
    set('Target', 'oms_cluster,opm_cluster')

    cd('/Library/gw-common#11.1.1@11.1.1')
    set('Target', 'oms_cluster,opm_cluster')
    #-------------------------------------------------------------
    # Domain Configuration
    print 'Setting domain configuration...'
    cd('/')
    set('Name', domain_name)
    cd('/SecurityConfiguration/base_domain')
    set('CredentialEncrypted', ces.encrypt(admin_pass))
    set('Name', domain_name)
    set('NodeManagerPasswordEncrypted', ces.encrypt(admin_pass))
    set('NodeManagerUsername', 'weblogic')
    #-------------------------------------------------------------
    # AdminServer configuration
    print 'Setting AdminServer configuration...'
    cd('/Servers/AdminServer')
    set('ListenAddress',admin_server_ip)
    set('ListenPort', admin_server_port)
    set('StagingDirectoryName', domain_path + '/' + domain_name + '/servers/AdminServer/stage')
    create('AdminServer', 'SSL')
    cd('SSL/AdminServer')
    set('ListenPort', admin_server_ssl_port)
    set('Enabled', true)
    #-------------------------------------------------------------
    # OAM server configuration
    print 'Setting OAM server configuration...'
    cd('/Servers/oam_server1')
    set('ListenAddress', oam_server_ip)
    set('ListenPort', oam_server_port)
    set('Machine', machine_name)
    set('Cluster', 'oam_cluster')
    create('oam_server1', 'JTAMigratableTarget')
    cd('JTAMigratableTarget/oam_server1')
    set('Cluster', 'oam_cluster')
    set('UserPreferredServer', 'oam_server1')
    cd('/Servers/oam_server1/SSL/oam_server1')
    set('Enabled', true)
    set('ListenPort', oam_server_ssl_port)
    #-------------------------------------------------------------
    # OMSM server configuration
    print 'Setting OMSM server configuration...'
    cd('/Servers/omsm_server1')
    set('ListenAddress', oms_server_ip)
    set('ListenPort', oms_server_port)
    set('Machine', machine_name)
    set('Cluster', 'oms_cluster')
    create('omsm_server1', 'JTAMigratableTarget')
    cd('JTAMigratableTarget/omsm_server1')
    set('Cluster', 'oms_cluster')
    set('UserPreferredServer', 'omsm_server1')
    cd('/Servers/omsm_server1/SSL/omsm_server1')
    set('Enabled', true)
    set('ListenPort', oms_server_ssl_port)
    #-------------------------------------------------------------
    # Policy Manager server configuration
    print 'Setting Policy Manager server configuration...'
    cd('/Servers/oam_policy_mgr1')
    set('ListenAddress',opm_server_ip)
    set('ListenPort', opm_server_port)
    set('Machine', machine_name)
    set('Cluster', 'opm_cluster')
    create('oam_policy_mgr1', 'JTAMigratableTarget')
    cd('JTAMigratableTarget/oam_policy_mgr1')
    set('Cluster', 'opm_cluster')
    set('UserPreferredServer', 'oam_policy_mgr1')
    cd('/Servers/oam_policy_mgr1/SSL/oam_policy_mgr1')
    set('Enabled', true)
    set('ListenPort', opm_server_ssl_port)
    #-------------------------------------------------------------
    # JDBC Datasources configuration
    #-------------------------------------------------------------
    # OPSS-DB
    print 'Setting Datasources configuration...'
    cd('/JDBCSystemResource/opss-DBDS')
    set('DeploymentOrder', 100)
    set('DescriptorFileName', 'jdbc/opss-jdbc.xml')
    set('Name', 'opss-DBDS')
    set('Target', 'oam_cluster,oms_cluster,opm_cluster,AdminServer')

    cd('/JDBCSystemResource/opss-DBDS/JdbcResource/opss-DBDS/JDBCConnectionPoolParams/NO_NAME_0')
    set('TestTableName', 'SQL SELECT 1 FROM DUAL')

    cd('/JDBCSystemResource/opss-DBDS/JdbcResource/opss-DBDS/JDBCDataSourceParams/NO_NAME_0')
    set('JNDIName', 'jdbc/OPSSDBDS')

    cd('/JDBCSystemResource/opss-DBDS/JdbcResource/opss-DBDS/JDBCDriverParams/NO_NAME_0')
    set('DriverName', 'oracle.jdbc.OracleDriver')
    set('PasswordEncrypted', database_opss_pass)
    set('URL', 'jdbc:oracle:thin:@' + database_host + ':' + database_port + '/' + database_service)

    create('myProperties','Properties')
    cd('Properties/NO_NAME_0/Property/user')
    set('Value', database_opss_schema)
    #-------------------------------------------------------------
    # MDS-OWSM
    cd('/JDBCSystemResource/mds-owsm')
    set('DeploymentOrder', 100)
    set('DescriptorFileName', 'jdbc/mds-owsm-jdbc.xml')
    set('Name', 'mds-owsm')
    set('Target', 'oms_cluster')

    cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm/JDBCConnectionPoolParams/NO_NAME_0')
    set('ConnectionCreationRetryFrequencySeconds',10)
    set('InitialCapacity', 0)
    set('SecondsToTrustAnIdlePoolConnection', 0)
    set('TestConnectionsOnReserve',true)
    set('TestFrequencySeconds', 300)
    set('TestTableName', 'SQL SELECT 1 FROM DUAL')

    cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm/JDBCDataSourceParams/NO_NAME_0')
    set('GlobalTransactionsProtocol', 'None')
    set('JNDIName', 'jdbc/mds/owsm')

    cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm/JDBCDriverParams/NO_NAME_0')
    set('DriverName', 'oracle.jdbc.OracleDriver')
    set('PasswordEncrypted', database_mds_pass)
    set('URL', 'jdbc:oracle:thin:@' + database_host + ':' + database_port + '/' + database_service)

    create('myProperties','Properties')
    cd('Properties/NO_NAME_0/Property/user')
    set('Value', database_mds_schema)

    cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm/JDBCDriverParams/NO_NAME_0')

    create('oracle.net.CONNECT_TIMEOUT','Properties')
    cd('Properties/NO_NAME_0/Property/oracle.net.CONNECT_TIMEOUT')
    set('Value', '10000')

    cd('/JDBCSystemResource/mds-owsm/JdbcResource/mds-owsm/JDBCDriverParams/NO_NAME_0')
    create('SendStreamAsBlob','Properties')
    cd('Properties/NO_NAME_0/Property/SendStreamAsBlob')
    set('Value', true)
    #-------------------------------------------------------------
    # OAM-DS
    cd('/JDBCSystemResource/oamDS')
    set('DeploymentOrder', 100)
    set('DescriptorFileName', 'jdbc/oam-db-jdbc.xml')
    set('Name', 'oamDS')
    set('Target', 'oam_cluster,opm_cluster,AdminServer')

    cd('/JDBCSystemResource/oamDS/JdbcResource/oamDS/JDBCConnectionPoolParams/NO_NAME_0')
    set('CapacityIncrement',1)
    set('ConnectionCreationRetryFrequencySeconds', 10)
    set('InactiveConnectionTimeoutSeconds',300)
    set('InitialCapacity', 20)
    set('MaxCapacity', 100)
    set('SecondsToTrustAnIdlePoolConnection',0)
    set('TestConnectionsOnReserve', true)
    set('TestFrequencySeconds', 300)
    set('TestTableName', 'SQL SELECT 1 FROM DUAL')

    cd('/JDBCSystemResource/oamDS/JdbcResource/oamDS/JDBCDataSourceParams/NO_NAME_0')
    set('GlobalTransactionsProtocol', 'OnePhaseCommit')
    set('JNDIName', 'jdbc/oamds')

    cd('/JDBCSystemResource/oamDS/JdbcResource/oamDS/JDBCDriverParams/NO_NAME_0')
    set('DriverName', 'oracle.jdbc.OracleDriver')
    set('PasswordEncrypted', database_oam_pass)
    set('URL', 'jdbc:oracle:thin:@' + database_host + ':' + database_port + '/' + database_service)

    create('myProperties','Properties')
    cd('Properties/NO_NAME_0/Property/user')
    set('Value', database_oam_schema)

    cd('/JDBCSystemResource/oamDS/JdbcResource/oamDS/JDBCDriverParams/NO_NAME_0')

    create('oracle.net.CONNECT_TIMEOUT','Properties')
    cd('Properties/NO_NAME_0/Property/oracle.net.CONNECT_TIMEOUT')
    set('Value', '10000')
    #-------------------------------------------------------------
    # OMSM-DS
    cd('/JDBCSystemResource/omsm-ds')
    set('DeploymentOrder', 100)
    set('DescriptorFileName', 'jdbc/omsm-db-jdbc.xml')
    set('Name', 'omsm-ds')
    set('Target', 'oms_cluster,opm_cluster')

    cd('/JDBCSystemResource/omsm-ds/JdbcResource/omsm-ds/JDBCConnectionPoolParams/NO_NAME_0')
    set('CapacityIncrement',1)
    set('ConnectionCreationRetryFrequencySeconds', 10)
    set('InitialCapacity', 0)
    set('MaxCapacity', 50)
    set('SecondsToTrustAnIdlePoolConnection',0)
    set('TestConnectionsOnReserve', true)
    set('TestFrequencySeconds', 300)
    set('TestTableName', 'SQL SELECT 1 FROM DUAL')

    cd('/JDBCSystemResource/omsm-ds/JdbcResource/omsm-ds/JDBCDataSourceParams/NO_NAME_0')
    set('GlobalTransactionsProtocol', 'None')
    set('JNDIName', 'jdbc/omsm-ds')

    cd('/JDBCSystemResource/omsm-ds/JdbcResource/omsm-ds/JDBCDriverParams/NO_NAME_0')
    set('DriverName', 'oracle.jdbc.OracleDriver')
    set('PasswordEncrypted', database_omsm_pass)
    set('URL', 'jdbc:oracle:thin:@' + database_host + ':' + database_port + '/' + database_service)

    create('myProperties','Properties')
    cd('Properties/NO_NAME_0/Property/user')
    set('Value', database_omsm_schema)

    cd('/JDBCSystemResource/omsm-ds/JdbcResource/omsm-ds/JDBCDriverParams/NO_NAME_0')

    create('oracle.net.CONNECT_TIMEOUT','Properties')
    cd('Properties/NO_NAME_0/Property/oracle.net.CONNECT_TIMEOUT')
    set('Value', '10000')
    #-------------------------------------------------------------
    # MDS-OAM
    cd('/JDBCSystemResource/mds-oam')
    set('DeploymentOrder', 100)
    set('DescriptorFileName', 'jdbc/mds-oam-jdbc.xml')
    set('Name', 'mds-oam')
    set('Target', 'opm_cluster')

    cd('/JDBCSystemResource/mds-oam/JdbcResource/mds-oam/JDBCConnectionPoolParams/NO_NAME_0')
    set('ConnectionCreationRetryFrequencySeconds', 10)
    set('InitialCapacity', 0)
    set('SecondsToTrustAnIdlePoolConnection',0)
    set('TestConnectionsOnReserve', true)
    set('TestFrequencySeconds', 300)
    set('TestTableName', 'SQL SELECT 1 FROM DUAL')

    cd('/JDBCSystemResource/mds-oam/JdbcResource/mds-oam/JDBCDataSourceParams/NO_NAME_0')
    set('GlobalTransactionsProtocol', 'None')
    set('JNDIName', 'jdbc/mds/oam')

    cd('/JDBCSystemResource/mds-oam/JdbcResource/mds-oam/JDBCDriverParams/NO_NAME_0')
    set('DriverName', 'oracle.jdbc.OracleDriver')
    set('PasswordEncrypted', database_mds_pass)
    set('URL', 'jdbc:oracle:thin:@' + database_host + ':' + database_port + '/' + database_service)

    create('myProperties','Properties')
    cd('Properties/NO_NAME_0/Property/user')
    set('Value', database_mds_schema)

    cd('/JDBCSystemResource/mds-oam/JdbcResource/mds-oam/JDBCDriverParams/NO_NAME_0')

    create('oracle.net.CONNECT_TIMEOUT','Properties')
    cd('Properties/NO_NAME_0/Property/oracle.net.CONNECT_TIMEOUT')
    set('Value', '10000')

    cd('/JDBCSystemResource/mds-oam/JdbcResource/mds-oam/JDBCDriverParams/NO_NAME_0')
    create('SendStreamAsBlob','Properties')
    cd('Properties/NO_NAME_0/Property/SendStreamAsBlob')
    set('Value', true)
    #-------------------------------------------------------------
    # Security configuration
    print 'Setting domain Security configuration...'
    cd('/Security/' + domain_name + '/User/weblogic')
    cmo.setPassword(admin_pass)

    setOption('OverwriteDomain', 'true')
    setOption('ServerStartMode','dev')
    #-------------------------------------------------------------
    # Write domain and close template
    print 'Writing domain...'
    writeDomain(domain_path + '/' + domain_name)
    closeTemplate()
    #-------------------------------------------------------------
    # Post Scrip Commands
    #-------------------------------------------------------------
    # Create application folder and copy EM ear
    print 'Creating Applications directoty and copying EM package...'
    if not os.path.exists(applications_path):
        os.makedirs(applications_path + '/' + domain_name)
    copyfile(mw_home + '/oracle_common/sysman/archives/fmwctrl/app/em.ear', applications_path + '/' + domain_name + '/em.ear')
    # Run Security Store configuration
    print 'Domain creating done...'
#-------------------------------------------------------------
# Checks if OAM is already configured in this container
if not os.path.exists(domain_path + '/' + domain_name):
    print 'Configuring new OAM domain...'
    configureOAMDomain()
else:
    print 'OAM domain configured, skipping OAM domain creation'
# Exit script
print 'Exiting WLST...'
exit()
