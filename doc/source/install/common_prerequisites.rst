Prerequisites
-------------

Before you install and configure the Cyborg Python Client service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``cyborgclient`` database:

     .. code-block:: none

        CREATE DATABASE cyborgclient;

   * Grant proper access to the ``cyborgclient`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON cyborgclient.* TO 'cyborgclient'@'localhost' \
          IDENTIFIED BY 'CYBORGCLIENT_DBPASS';
        GRANT ALL PRIVILEGES ON cyborgclient.* TO 'cyborgclient'@'%' \
          IDENTIFIED BY 'CYBORGCLIENT_DBPASS';

     Replace ``CYBORGCLIENT_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``cyborgclient`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt cyborgclient

   * Add the ``admin`` role to the ``cyborgclient`` user:

     .. code-block:: console

        $ openstack role add --project service --user cyborgclient admin

   * Create the cyborgclient service entities:

     .. code-block:: console

        $ openstack service create --name cyborgclient --description "Cyborg Python Client" cyborg python client

#. Create the Cyborg Python Client service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        cyborg python client public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        cyborg python client internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        cyborg python client admin http://controller:XXXX/vY/%\(tenant_id\)s
