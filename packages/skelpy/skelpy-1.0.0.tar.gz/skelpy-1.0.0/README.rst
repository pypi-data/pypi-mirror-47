*skelpy* is a simple template tool to create the directory structure for
python projects. In addition to creating basic directories for a project,
*skelpy* generates several configuration files for widely-used tools.
Those include:

    * ``setup.py`` and ``setup.cfg`` for `setuptools <https://setuptools.readthedocs.io/en/latest/>`_
    * ``conf.py``, ``index.rst`` for `sphinx <http://www.sphinx-doc.org/en/master/>`_ documentation

For the complete directory structure and files for *skelpy* to create, see `quick_start`_

Features
========

OS Independent
--------------
*skelpy* supports Linux, Windows, OSX and Cygwin.

No Dependency
-------------
*skelpy* was written in pure python and requires no extra library or module
unless you want to run the test codes of *skelpy* yourself.
In that case, you will need `pytest <https://docs.pytest.org/en/latest/>`_
and `mock <https://pypi.org/project/mock/>`_ (only if you use python 2.7 and
3.3 downward)

.. note::

    mock is now part of the Python standard library, available as unittest.mock in Python 3.3 onwards.

Support python 2.7 and 3.x
--------------------------
*skelpy* works well on python 2.7 and 3.x.

Install
=======

From PyPi
---------
On the command line, just type either of belows::

    pip install skelpy
    or
    pip install --user skelpy

The first one is for system-wide installation and you may need the administrator
/root privilege. The second command will install *skelpy* in the user's python
install directory, which is ~/.local/ on linux and Mac,
%APPDATA%\Python on Windows.

From Git
--------
Another option is to download *skelpy*'s source codes using ``git`` and to build an
executable zip file. *skelpy*'s ``setup.py`` can build the zip-formatted executable.
To do that, run the command below in order::

    $ git clone https://github.com/june3474/skelpy.git
    $ cd skelpy
    $ python setup.py ezip

Now you will be able to find an excutable zip file named ``skelpy.zip``
in the ``dist`` directory .
Once got the zip file--changing the name of the zip file is OK--,
you can directly run the zip file as if it were a python module like below::

    python skelpy.zip [options_for_skelpy] [project_name_to_create]


Or, if you use Linux or any POSIX-compatible OS, you can make the zip file an executable::

    $ echo '#!/usr/bin/env python' > skelpy
    $ cat skelpy-master.zip >> skelpy
    $ chmod u+x skelpy

Codes above are from "The Hitchhiker's Guide to Python" by Kenneth Reitz and Tanya Schlusser.

.. _quick_start:

Quick Start
===========

To start a new project, say 'my_project', just type on the command line ::
  
   skelpy my_project

This will create a new folder ``my_project`` under the current directory and
fill the directory with sub-directories and configuration files like below::

    'basic' format(default)                   'src' format

    my_project/                               my_project/
    ├── docs/                                 ├── docs/
    │   ├── _build/                           │   ├── _build/
    │   ├── _static/                          │   ├── _static/
    │   ├── _templates/                       │   ├── _templates/
    │   ├── conf.py                           │   ├── conf.py
    │   ├── index.rst                         │   ├── index.rst
    │   ├── make.bat                          │   ├── make.bat
    │   └── Makefile                          │   └── Makefile
    ├── my_project/                           ├── src/
    │   ├── __init__.py                       │   └── my_project/
    │   └── main.py                           │       ├── __init__.py
    ├── tests/                                │       └── main.py
    │    └── test_main.py                     ├── tests/
    ├── LICENSE                               │    └── test_main.py
    ├── README.rst                            ├── LICENSE
    ├── setup.cfg                             ├── README.rst
    └── setup.py                              ├── setup.cfg
                                              └── setup.py

You can choose which tructure to use with the ``--format/-f`` option.
Also, if you do not provide the project name, *skelpy* will consider
the current directory name(the last component of the current working directory)
to be the project name.

For more options, See ``skelpy -h``

License
=======
*skelpy* is under the `MIT`_ license.

Author
======
dks <june3474@gmail.com>

Change Log
==========
## [1.0.rc0] - 2019-04-13

## [1.0.0]   - 2019-05-31

Reference
=========
Reference is available at 
`https://june3474.github.io/skelpy/api/modules.html <https://june3474.github.io/skelpy/api/modules.html>`_

.. _Pyscaffold: https://pyscaffold.org/en/latest/
.. _Cookiecutter: https://cookiecutter.readthedocs.org/
.. _MIT: https://choosealicense.com/licenses/mit/
