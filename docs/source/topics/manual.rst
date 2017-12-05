User Manual
===========

Usage
-----

    $ wallter [-L LOGFILE]

The first argument is the desired datastore url. The remaining arguments are
optional.

- ``-h`` ``--help`` Shows usage text
- ``-V`` ``--version`` Displays the version of the application and exits
- ``-l`` ``--log-level`` Set logging level (DEBUG, INFO, WARN, etc...)
- ``-L`` ``--logfile`` Logfile location


.. top:: If a logfile location is not set, no output will be logged, but
    messages will still appear in the console.

Example::

    $ wallter -L /home/brant/output.log
