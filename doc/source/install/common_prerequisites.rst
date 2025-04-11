Prerequisites
-------------

Before you install and configure the aetos service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``aetos`` database:

     .. code-block:: none

        CREATE DATABASE aetos;

   * Grant proper access to the ``aetos`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON aetos.* TO 'aetos'@'localhost' \
          IDENTIFIED BY 'AETOS_DBPASS';
        GRANT ALL PRIVILEGES ON aetos.* TO 'aetos'@'%' \
          IDENTIFIED BY 'AETOS_DBPASS';

     Replace ``AETOS_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``aetos`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt aetos

   * Add the ``admin`` role to the ``aetos`` user:

     .. code-block:: console

        $ openstack role add --project service --user aetos admin

   * Create the aetos service entities:

     .. code-block:: console

        $ openstack service create --name aetos --description "aetos" aetos

#. Create the aetos service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        aetos public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        aetos internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        aetos admin http://controller:XXXX/vY/%\(tenant_id\)s
