=========================
Enabling Aetos in DevStack
=========================

1. Download DevStack::

    git clone https://opendev.org/openstack/devstack.git
    cd devstack

2. Add this repo as an external repository in ``local.conf`` file::

    [[local|localrc]]
    enable_plugin aetos https://opendev.org/openstack/aetos

   To use stable branches, make sure devstack is on that branch, and specify
   the branch name to enable_plugin, for example::

    enable_plugin aetos https://opendev.org/openstack/aetos stable/2025.1

   There are some options, defined in
   ``aetos/devstack/settings``, they can be used to configure the installation
   of Aetos. If you don't want to use their default value, you can set a new
   one in ``local.conf``.

3. Run ``stack.sh``.
