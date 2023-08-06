################################################
``metlinkpid-http``: HTTP server for Metlink PID
################################################

..  image:: https://img.shields.io/pypi/v/metlinkpid-http.svg
    :target: https://pypi.org/project/metlinkpid-http
    :alt: latest release on PyPI

The ``metlinkpid-http`` script
provides an HTTP endpoint for a Metlink LED passenger information display::

    $ metlinkpid-http --serial=/dev/ttyUSB0
    Serving on http://127.0.0.1:8080

    $ curl 'http://127.0.0.1:8080?12:34+FUNKYTOWN~5|Limited+Express|_Stops+all+stations+except+East+Richard'
    {"error":null,"message":"12:34 FUNKYTOWN~5|Limited Express|_Stops all stations except East Richard"}


Installation
============

Install from PyPI_ using pip_::

    pip install metlinkpid-http

..  _PyPI: https://pypi.org/project/metlinkpid-http
..  _pip: https://pip.pypa.io/


Basic usage
===========

Find the device
---------------

Determine the device to which the display is connected.
On Linux, this can be achieved by disconnecting the display from the computer & reconnecting,
then inspecting the contents of ``dmesg`` output for USB attachment messages::

    [    3.010816] usb 1-1.4: FTDI USB Serial Device converter now attached to ttyUSB0

The above output indicates that the display is reachable through ``/dev/ttyUSB0``.

Start the HTTP server
---------------------

Run the script passing that device location as the ``--serial`` option::

    $ metlinkpid-http --serial=/dev/tty/USB0

The script accepts the following options:

``--serial=PORT``
    The PID serial device name,
    such as ``/dev/ttyUSB0`` on Linux or ``COM1`` on Windows.
    If not specified, defaults to the value of environment variable ``METLINKPID_SERIAL``;
    if no such variable, defaults to ``/dev/ttyUSB0``.

``--http=HOST:PORT``
    The hostname/IP address and port to listen on, separated by a colon (``:``).
    If not specified, defaults to the value of environment variable ``METLINKPID_HTTP``;
    if no such variable, defaults to ``127.0.0.1:8080``.

``-h`` or ``--help``
    Displays usage information similar to above,
    and provides a link to this documentation.

If the PID successfully connects, the URL is confirmed::

    Serving on http://127.0.0.1:8080


Display a message
-----------------

Next, browse to the specified URL in a browser,
adding an `appropriately encoded query string`_ to the end:

    http://127.0.0.1:8080?MY+MESSAGE

You should see a plain-text JSON result similar to this::

    {"error":null,"message":"MY MESSAGE"}

The same result can be obtained on the terminal using ``curl``::

    $ curl 'http://127.0.0.1:8080?MY+MESSAGE'
    {"error":null,"message":"MY MESSAGE"}

You could do the same thing in Python like this, using the `"requests" library`_:

>>> import requests
>>> requests.get('http://127.0.0.1:8080?MY+MESSAGE').json()
{'error': None, 'message': 'MY MESSAGE'}

By exposing the display via HTTP in this way,
you can operate it using almost any programming language or toolkit.

See the `"metlinkpid" module documentation`_
for full details about message formatting.

The HTTP server also periodically pings the display in the background,
preventing message display timeout.

..  _appropriately encoded query string:
    https://en.wikipedia.org/wiki/Percent-encoding#Percent-encoding_in_a_URI
..  _"requests" library:
    https://2.python-requests.org
..  _"metlinkpid" module documentation:
    https://python-metlinkpid.readthedocs.io


Support
=======

Bug reports, feature requests, and questions are welcome via the issue tracker.

:Issue tracker: https://github.com/Lx/python-metlinkpid-http/issues


Contribute
==========

Pull requests for both code and documentation improvements
are gratefully received and considered.

:GitHub repository: https://github.com/Lx/python-metlinkpid-http


License
=======

This project is licensed under the `MIT License`_.

..  _MIT License: https://opensource.org/licenses/MIT
