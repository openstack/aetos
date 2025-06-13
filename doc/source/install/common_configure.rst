2. Edit the ``/etc/aetos/aetos.conf`` file and complete the following
   actions:

   * In the ``[DEFAULT]`` section, configure prometheus access:

     .. code-block:: ini

        [DEFAULT]
        prometheus_host=localhost
        prometheus_port=9090

   * In the ``[DEFAULT]`` and ``[keystone_authtoken]`` sections,
     configure Identity service access:

     .. code-block:: ini

        [DEFAULT]
        ...
        auth_strategy = keystone

        [keystone_authtoken]
        ...
        www_authenticate_uri = http://controller:5000
        auth_url = http://controller:5000
        memcached_servers = controller:11211
        auth_type = password
        project_domain_id = default
        user_domain_id = default
        project_name = service
        username = aetos
        password = AETOS_PASS

     Replace ``AETOS_PASS`` with the password you chose for
     the ``aetos`` user in the Identity service.
