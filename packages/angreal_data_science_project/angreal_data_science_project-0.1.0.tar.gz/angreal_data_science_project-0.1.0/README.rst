#####################
Data Science Project
#####################


An angreal for data science projects. It uses several docker images provided by from vila_ in order to allow work to be
completely portable. Designed with fostering good enough software engineering practices in place so that research and
production move closer together.


.. _vila: https://hub.docker.com/r/dockerrepay/vilya


Usage
#####

Assuming you already have the angreal_ program installed on your computer :

.. _angreal: https://angreal.gitlab.io/angreal

.. code-block:: bash

    angreal init data_science_project


.. image:: /docs/images/angreal_init.gif




Features
########

* Tensor flow with gpu support.

* Jupyter Lab instances


.. image:: /docs/images/angreal_nb.gif



* Jupyter Kernel loads your python module at start and keeps it fresh if you make edits.

.. image:: /docs/images/nb_reload.gif


* Project administration (tests, documentation, static typing) in local environment or in container.


.. image:: /docs/images/angreal_tests.gif



Configuration Options
######################

All configuration options are prompted and set via templating. The last option (`tensorflow_string`) should not be edited,
just hit enter.


Commands/Functions Provided
############################


.. code-block:: bash

    Usage: angreal [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Project Commands:
      docs         compile documentation for the project
      integration  run tests in tests/integration
      nb           launch the jupyter lab notebook
      setup        update or create the virtual environment
      static       run static typing tests via mypy
      tests        run tests in tests/unit


setup
-----

Setup a virtual environment at ~/.venv/<project_name> using your requirments files.

.. code-block:: bash

    Usage: angreal setup [OPTIONS]

      update or create the virtual environment

    Options:
      --no_dev   Do not setup the dev requirements
      --help     Show this message and exit.


nb
--

Launch a notebook server, by default if GPUs are available it will launch a GPU server instance. The `project` dir is bound
to the root of the actual project so edits in container are persisted locally. A password can be set at run time for
some semblance of security.

On exit - files aren't committed a warning will be produced.

.. code-block:: bash

    Usage: angreal nb [OPTIONS]

      launch the jupyter lab notebook

    Options:
      --verbose        Verbose outputs get you logs from build and container.
      --no_open        Don't attempt to open my jupyter lab instance.
      --password TEXT  Token to use for security
      --cpu            Force usage of CPU
      --help           Show this message and exit.


tests
-----

Run unit tests. By default a container is built and launched for this. If you wish to run in a local environment use the
``--no_docker`` option.


.. code-block:: bash

    Usage: angreal tests [OPTIONS]

      run tests in tests/unit

    Options:
      --verbose    Verbose outputs get you logs from build and container.
      --cpu        Force usage of CPU
      --no_docker  Don't attempt to run inside of a docker container
      --help       Show this message and exit.

docs
-----

Generate your docs via sphinx.

.. code-block:: bash

    Usage: angreal docs [OPTIONS]

      compile documentation for the project

    Options:
      --verbose    Verbose outputs get you logs from build and container.
      --cpu        Force usage of CPU
      --no_docker  Don't attempt to run inside of a docker container
      --help       Show this message and exit.


static
-------

Generate a static typing report.

.. code-block:: bash

    Usage: angreal static [OPTIONS]

      run static typing tests via mypy

    Options:
      --verbose    Verbose outputs get you logs from build and container.
      --cpu        Force usage of CPU
      --no_docker  Don't attempt to run inside of a docker container
      --help       Show this message and exit.


integration
------------

Same as `tests` but intended for integration/functional tests.

.. code-block:: bash

    Usage: angreal integration [OPTIONS]

      run tests in tests/integration

    Options:
      --verbose    Verbose outputs get you logs from build and container.
      --cpu        Force usage of CPU
      --no_docker  Don't attempt to run inside of a docker container
      --help       Show this message and exit.
