2. Edit the ``/etc/aetos/aetos.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://aetos:AETOS_DBPASS@controller/aetos
