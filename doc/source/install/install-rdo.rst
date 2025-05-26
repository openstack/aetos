.. _install-rdo:

Install and configure for Red Hat Enterprise Linux and CentOS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


This section describes how to install and configure the aetos service
for Red Hat Enterprise Linux 9 and CentOS Stream 9.

.. include:: common_prerequisites.rst

Install and configure components
--------------------------------

#. Install the packages:

   .. code-block:: console

      # dnf install openstack-aetos-api

.. include:: common_configure.rst

Finalize installation
---------------------

Start the aetos services and configure them to start when
the system boots:

.. code-block:: console

   # systemctl enable openstack-aetos-api.service

   # systemctl start openstack-aetos-api.service
