Aetos Sample Configuration File
===============================

Configure Aetos by editing /etc/aetos/aetos.conf.

No config file is provided with the source code, it will be created during
the installation. In case where no configuration file was installed, one
can be easily created by running::

    oslo-config-generator \
        --config-file=/etc/aetos/aetos-config-generator.conf \
        --output-file=/etc/aetos/aetos.conf


.. only:: html

   The following is a sample Aetos configuration for adaptation and use.
   It is auto-generated from Aetos when this documentation is built, and
   can also be viewed in `file form <../_static/aetos.conf.sample>`_.

   .. literalinclude:: ../_static/aetos.conf.sample

