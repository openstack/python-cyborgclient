2. Edit the ``/etc/cyborgclient/cyborgclient.conf`` file and complete the following
   actions:

   * In the ``[database]`` section, configure database access:

     .. code-block:: ini

        [database]
        ...
        connection = mysql+pymysql://cyborgclient:CYBORGCLIENT_DBPASS@controller/cyborgclient
