=============
Examine Files
=============


.. image:: https://img.shields.io/pypi/v/examine_files.svg
        :target: https://pypi.python.org/pypi/examine_files

.. image:: https://img.shields.io/travis/hobnobpirate/examine_files.svg
        :target: https://travis-ci.org/hobnobpirate/examine_files

.. image:: https://readthedocs.org/projects/examine-files/badge/?version=latest
        :target: https://examine-files.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Checks to see if magic number contents of files match extensions. Mostly a CTF tool.


* Free software: MIT license
* Documentation: https://examine-files.readthedocs.io.


Features
--------

* Utilizes libmagic to analyze file type
* Compares analyzed file type with expected type based on file extension
* Prints report of matches, mismatches, and unknown status
* Accepts custom whitelist or utilizes built-in default for demonstration only

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

The core functionality for this script relies on python-magic_ by Adam Hupp.
For installation questions outside of Linux (or the provided docker container), please see https://github.com/ahupp/python-magic.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _python-magic: https://github.com/ahupp/python-magic