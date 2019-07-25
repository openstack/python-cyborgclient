========================
Team and repository tags
========================

.. image:: https://governance.openstack.org/tc/badges/python-cyborgclient.svg
    :target: https://governance.openstack.org/tc/reference/tags/index.html

.. Change things from this point on

===============================
python-cyborgclient
===============================

.. image:: https://img.shields.io/pypi/v/python-cyborgclient.svg
    :target: https://pypi.python.org/pypi/python-cyborgclient/
    :alt: Latest Version

python-cyborgclient is a python bindings to the OpenStack Cyborg API. There's
a Python API (the ``cyborgclient`` module), and a command-line script
(``cyborg``). Each implements 100% of the OpenStack Cyborg API.

See the `OpenStack CLI Reference`_ for information on how to use the ``cyborg``
command-line tool. You may also want to look at the
`OpenStack API documentation`_.

.. _OpenStack CLI Reference: https://docs.openstack.org/python-openstackclient/latest/cli/
.. _OpenStack API documentation: https://docs.openstack.org/api-quick-start/

The project is hosted on `Launchpad`_, where bugs can be filed. The code is
hosted on `OpenStack`_. Patches must be submitted using `Gerrit`_.

.. _OpenStack: https://git.openstack.org/cgit/openstack/python-cyborgclient
.. _Launchpad: https://launchpad.net/python-cyborgclient
.. _Gerrit: https://docs.openstack.org/infra/manual/developers.html#development-workflow

This code is a fork of `Jacobian's python-cloudservers`__. If you need API support
for the Rackspace API solely or the BSD license, you should use that repository.
python-cyborgclient is licensed under the Apache License like the rest of OpenStack.

__ https://github.com/jacobian-archive/python-cloudservers

* License: Apache License, Version 2.0
* `PyPi`_ - package installation
* `Online Documentation`_
* `Blueprints`_ - feature specifications
* `Bugs`_ - issue tracking
* `Source`_
* `Specs`_
* `How to Contribute`_

.. _PyPi: https://pypi.python.org/pypi/python-cyborgclient
.. _Online Documentation: https://docs.openstack.org/python-cyborgclient/latest/
.. _Blueprints: https://blueprints.launchpad.net/python-cyborgclient
.. _Bugs: https://bugs.launchpad.net/python-cyborgclient
.. _Source: https://git.openstack.org/cgit/openstack/python-cyborgclient
.. _How to Contribute: https://docs.openstack.org/infra/manual/developers.html
.. _Specs: https://specs.openstack.org/openstack/cyborg-specs/


.. contents:: Contents:
   :local:


Command-line API
----------------

Installing this package gets you a shell command, ``cyborg``, that you
can use to interact with any Rackspace compatible API (including OpenStack).

You'll need to provide your OpenStack username and password. You can do this
with the ``--os-username``, ``--os-password`` and  ``--os-tenant-name``
params, but it's easier to just set them as environment variables::

    export OS_USERNAME=openstack
    export OS_PASSWORD=yadayada
    export OS_TENANT_NAME=myproject

You will also need to define the authentication url with ``--os-auth-url``
and the version of the API with ``--os-accelerator-api-version``. Or set them
as environment variables as well, ``OS_ACCELERATOR_API_VERSION=1``. If you
are using Keystone, you need to set the ``OS_AUTH_URL`` to the keystone
endpoint::

    export OS_AUTH_URL=http://controller:5000/v3
    export OS_ACCELERATOR_API_VERSION=1

Since Keystone can return multiple regions in the Service Catalog, you
can specify the one you want with ``--os-region-name`` (or
``export OS_REGION_NAME``). It defaults to the first in the list returned.

You'll find complete documentation on the shell by running
``cyborg help``


Python API
----------

There's also a complete Python API, but it has not yet been documented.

Quick-start using keystone::

    # pass auth plugin and session to Client init.
    # service_parameters contains servive_name, service_type, interface and
    # region name.
    >>> from cyborgclient.v1 import client
    >>> nt = client.Client(auth=auth,session=_SESSION,**service_parameters)
    >>> nt.accelerators.list()
    [...]

See release notes and more at `<https://docs.openstack.org/python-cyborgclient/latest/>`_.
