Stackformation
==============

|pypi| |travis| |codecov| |readocs| |pyup| |docker|

Cloudformation framework to support infrastructure-as-code paradigm

Installation
------------

``pip install jh-stackformation``

| Framework requires python >= 3.5.x and Hashicorp Packer in-order to
  build custom AMI's.
| Docker is the preferred method of execution ( all dependencies
  including packer are included ) however VirtualEnv works A-OK.
  Reference the demo repo below for examples and helper scripts using
  the docker images built on docker-hub.

Examples / Demo
---------------

| Examples and docker helper scripts can be found @
| https://github.com/ibejohn818/stackformation-demo

-  Free software: MIT license
-  Documentation: https://jh-stackformation.readthedocs.io.

TODO's
^^^^^^

-  

.. |pypi| image:: https://img.shields.io/pypi/v/jh-stackformation.svg
   :target: https://pypi.python.org/pypi/jh-stackformation
.. |travis| image:: https://travis-ci.org/ibejohn818/stackformation.svg?branch=master
   :target: https://travis-ci.org/ibejohn818/stackformation
.. |codecov| image:: https://codecov.io/gh/ibejohn818/stackformation/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/ibejohn818/stackformation
.. |readocs| image:: https://readthedocs.org/projects/jh-stackformation/badge/?version=latest
   :target: https://jh-stackformation.readthedocs.io/en/latest/?badge=latest
.. |pyup| image:: https://pyup.io/repos/github/ibejohn818/stackformation/shield.svg
   :target: https://pyup.io/repos/github/ibejohn818/stackformation/
.. |docker| image:: https://img.shields.io/docker/build/ibejohn818/stackformation.svg
   :target: https://hub.docker.com/r/ibejohn818/stackformation
