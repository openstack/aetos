Prerequisites
-------------

Before you install and configure the aetos service,
you must create service credentials, and API endpoints.

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``aetos`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt aetos
        User Password:
        Repeat User Password:
        +---------------------+----------------------------------+
        | Field               | Value                            |
        +---------------------+----------------------------------+
        | domain_id           | default                          |
        | enabled             | True                             |
        | id                  | b7657c9ea07a4556aef5d34cf70713a3 |
        | name                | aetos                            |
        | options             | {}                               |
        | password_expires_at | None                             |
        +---------------------+----------------------------------+

   * Add the ``admin`` role to the ``aetos`` user:

     .. code-block:: console

        $ openstack role add --project service --user aetos admin

     .. note::

        This command provides no output.


   * Create the aetos service entities:

     .. code-block:: console

        $ openstack service create --name aetos --description "OpenStack Aetos Service" metric-storage
        +-------------+----------------------------------+
        | Field       | Value                            |
        +-------------+----------------------------------+
        | description | OpenStack Aetos Service          |
        | enabled     | True                             |
        | id          | 3405453b14da441ebb258edfeba96d83 |
        | name        | aetos                            |
        | type        | metric-storage                   |
        +-------------+----------------------------------+

#. Create the aetos service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        metric-storage public http://controller/prometheus
        +--------------+-----------------------------------+
        | Field        | Value                             |
        +--------------+-----------------------------------+
        | enabled      | True                              |
        | id           | 1196727cc22a4a26a011688236c38da9  |
        | interface    | public                            |
        | region       | RegionOne                         |
        | region_id    | RegionOne                         |
        | service_id   | 3405453b14da441ebb258edfeba96d83  |
        | service_name | aetos                             |
        | service_type | metric-storage                    |
        | url          | http://controller/prometheus      |
        +--------------+-----------------------------------+
      $ openstack endpoint create --region RegionOne \
        metric-storage internal http://controller/prometheus
        +--------------+-----------------------------------+
        | Field        | Value                             |
        +--------------+-----------------------------------+
        | enabled      | True                              |
        | id           | 1196727cc22a4a26a011688236c38da9  |
        | interface    | internal                          |
        | region       | RegionOne                         |
        | region_id    | RegionOne                         |
        | service_id   | 3405453b14da441ebb258edfeba96d83  |
        | service_name | aetos                             |
        | service_type | metric-storage                    |
        | url          | http://controller/prometheus      |
        +--------------+-----------------------------------+
      $ openstack endpoint create --region RegionOne \
        metric-storage admin http://controller/prometheus
        +--------------+-----------------------------------+
        | Field        | Value                             |
        +--------------+-----------------------------------+
        | enabled      | True                              |
        | id           | 1196727cc22a4a26a011688236c38da9  |
        | interface    | admin                             |
        | region       | RegionOne                         |
        | region_id    | RegionOne                         |
        | service_id   | 3405453b14da441ebb258edfeba96d83  |
        | service_name | aetos                             |
        | service_type | metric-storage                    |
        | url          | http://controller/prometheus      |
        +--------------+-----------------------------------+
