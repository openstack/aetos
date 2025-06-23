==============================
Installing development sandbox
==============================

Configuring devstack
====================

.. index::
   double: installing; devstack

1. Download devstack_.

2. Create a ``local.conf`` file as input to devstack.

   .. note::

      ``local.conf`` replaces the former configuration file called ``localrc``.
      If you used localrc before, remove it to switch to using the new file.
      For further information see the `devstack configuration
      <https://docs.openstack.org/devstack/latest/configuration.html>`_.

3. The aetos service is not enabled by default, so it must be
   enabled in ``local.conf`` before running ``stack.sh``.

   This example ``local.conf`` file shows all of the settings required for
   aetos, as well as how to deploy ceilometer with prometheus, which is recommended::

      [[local|localrc]]
      # Configure Ceilometer to send metrics through sg-core to Prometheus
      CEILOMETER_BACKEND=sg-core

      # Configure Prometheus to scrape sg-core and itself
      PROMETHEUS_CUSTOM_SCRAPE_TARGETS="localhost:3000,localhost:9090"

      # Enable Ceilometer
      enable_plugin ceilometer https://opendev.org/openstack/ceilometer

      # Enable Prometheus
      enable_plugin devstack-plugin-prometheus https://opendev.org/openstack/devstack-plugin-prometheus

      # Enable sg-core for forwarding metrics from Ceilometer to Prometheus
      enable_plugin sg-core https://github.com/infrawatch/sg-core

      # Enable the Aetos
      enable_plugin aetos https://opendev.org/openstack/aetos

.. _devstack: https://docs.openstack.org/devstack/latest/

