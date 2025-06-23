===========================
Installing Aetos with uwsgi
===========================

The module ``aetos.wsgi.api`` provides the function to set up the WSGI
application. The module is installed with the rest of the Aetos application
code, and should not need to be modified.

Install uwsgi.

On RHEL/CentOS/Fedora::

    sudo dnf install uwsgi-plugin-python3

On Ubuntu/Debian::

    sudo apt-get install uwsgi-plugin-python3

Create aetos-uwsgi.ini file::

    [uwsgi]
    chmod-socket = 666
    socket = /var/run/uwsgi/aetos.socket
    start-time = %t
    lazy-apps = true
    add-header = Connection: close
    buffer-size = 65535
    hook-master-start = unix_signal:15 gracefully_kill_them_all
    thunder-lock = true
    plugins = http,python3
    enable-threads = true
    worker-reload-mercy = 80
    exit-on-reload = false
    die-on-term = true
    master = true
    processes = 2
    module = aetos.wsgi.api:application

Then start the uwsgi server::

    uwsgi ./aetos-uwsgi.ini

Or start in background with::

    uwsgi -d ./aetos-uwsgi.ini
