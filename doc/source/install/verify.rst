.. _verify:

Verify operation
~~~~~~~~~~~~~~~~

Verify operation of the aetos service.

.. note::

   Perform these commands on the controller node.

.. note::

   The following assumes Ceilometer is installed and Prometheus is
   configured to scrape metrics from Ceilometer. The
   ``ceilometer_image_size`` metric is used for the verification. A
   working Image service with an image stored is required to get the
   ``ceilometer_image_size`` metric.

#. Source the ``admin`` project credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. Query for the ceilometer_image_size metric and see if data is returned:

   .. code-block:: console

      $ openstack metric query ceilometer_image_size
      +----------+----------+----------+----------+---------+----------+-----------+----------+---------------+------+------+----------+
      | __name__ | counter  | image    | instance | job     | project  | publisher | resource | resource_name | type | unit | value    |
      +----------+----------+----------+----------+---------+----------+-----------+----------+---------------+------+------+----------+
      | ceilomet | image.si | 6b51fba6 | localhos | sg-core | 2dd8edd6 | localhost | 6b51fba6 | Fedora-Cloud- | size | B    | 49283072 |
      | er_image | ze       | -8b74-4b | t:3000   |         | c8c24f49 | .localdom | -8b74-4b | Base-37-1.7.x |      |      | 0        |
      | _size    |          | d4-be53- |          |         | bf046705 | ain       | d4-be53- | 86_64         |      |      |          |
      |          |          | 25e509ea |          |         | 34f6b357 |           | 25e509ea |               |      |      |          |
      |          |          | 0aaf     |          |         |          |           | 0aaf     |               |      |      |          |
      +----------+----------+----------+----------+---------+----------+-----------+----------+---------------+------+------+----------+
