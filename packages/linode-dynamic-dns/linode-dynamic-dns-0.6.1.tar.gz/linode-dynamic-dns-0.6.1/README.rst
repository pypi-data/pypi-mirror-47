linode-dynamic-dns
==================

|Version| |License|

Update Linode DNS records with your local IPv4 and IPv6 addresses.

Environment Variables
---------------------

+----------+-----------------------------------------------------------------------------------------+
| Name     | Description                                                                             |
+==========+=========================================================================================+
| HOST     | The host record to update.                                                              |
+----------+-----------------------------------------------------------------------------------------+
| DOMAIN   | The domain the host is a part of.                                                       |
+----------+-----------------------------------------------------------------------------------------+
| TOKEN    | Your Linode API access token.                                                           |
+----------+-----------------------------------------------------------------------------------------+
| IPV4_URL | The URL which returns your local IPv4 address (default ``https://ipv4.icanhazip.com/``) |
+----------+-----------------------------------------------------------------------------------------+
| IPV6_URL | The URL which returns your local IPv6 address (default ``https://ipv6.icanhazip.com/``) |
+----------+-----------------------------------------------------------------------------------------+


Installation
------------

* `Arch Linux`_
* `Docker`_
* `PyPI`_


.. |Version| image:: https://img.shields.io/pypi/v/linode-dynamic-dns.svg?
   :target: https://pypi.org/pypi/linode-dynamic-dns

.. |License| image:: https://img.shields.io/github/license/nvllsvm/linode-dynamic-dns.svg?
   :target: https://github.com/nvllsvm/linode-dynamic-dns/blob/master/LICENSE

.. _Arch Linux: https://aur.archlinux.org/packages/linode-dynamic-dns/
.. _Docker: https://hub.docker.com/r/nvllsvm/linode-dynamic-dns/
.. _PyPI: https://pypi.org/pypi/linode-dynamic-dns
