.. _installation:

Installing CPAC
===============

C-PAC is a containerized software package, running in `Docker <https://www.docker.com>`_ or `Singularity <https://sylabs.io/guides/3.1/user-guide/>`_. Releases and development Docker images are published on Docker Hub as ``fcpindi/c-pac:latest`` and ``fcpindi/c-pac:nightly``, respectively. Releases are also published on Singularity Hub as ``FCP-INDI/C-PAC``.

.. include:: installing.txt

Downloading the latest version of CPAC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. seealso::

    - :cpac_user:`User Documentation: C-PAC Quickstart <quick>`
    - :cpac_user:`User Documentation: Installing C-PAC <appendix#installing-c-pac>`


Building a C-PAC container image
================================

To build an image, you'll need `Docker <https://www.docker.com>`_ and/or `Singularity <https://sylabs.io/guides/3.1/user-guide/>`_. You'll also need adequate permissions on your machine (membership in the ``docker`` and/or ``sudo`` usergroups).

Docker
^^^^^^

Docker images are abstracted away and stored with Docker's program data. To build a Docker image with the tag ``$DOCKER_TAG``, just run the following code from the directory containing `Dockerfile <https://github.com/FCP-INDI/C-PAC/blob/master/Dockerfile>`_.

.. code-block:: shell

    docker build -t $DOCKER_IMAGE:$DOCKER_TAG [--no-cache] .


For example, to build an image ``fcpindi/c-pac`` with the tag ``example``:

.. code-block:: shell

    docker build -t fcpindi/c-pac:example [--no-cache] .


Singularity
^^^^^^^^^^^

Singularity images are stored in local files with an extension ``.simg`` in v2, ``.sif`` in v3. They can be built from Docker images or from Docker files.

From Docker image
-----------------

Singularity can build a Singularity image from a Docker image in a Docker registry. If you're not using an existing registry (e.g., Docker Hub), you can `run a local registry <https://docs.docker.com/registry/deploying/#run-a-local-registry>`_. To set a registry up

.. code-block:: shell

    docker run -d -p $DOCKER_REGISTRY_PORT:$DOCKER_REGISTRY_PORT --restart=always --name registry registry:2

Then tag and push your Docker image to your registry

.. code-block:: shell

    docker tag fcpindi/c-pac:$DOCKER_TAG $DOCKER_REGISTRY_HOST:$DOCKER_REGISTRY_PORT/fcpindi/c-pac:$DOCKER_TAG
    docker push $DOCKER_REGISTRY_HOST:$DOCKER_REGISTRY_PORT/$DOCKER_IMAGE:$DOCKER_TAG


Finally, you can build a Singularity image from your registered Docker image.  If you're using Docker Hub or some other HTTPS registry, you can omit ``SINGULARITY_NOHTTPS=1`` and ``$DOCKER_REGISTRY_HOST:$DOCKER_REGISTRY_PORT/`` when building

.. code-block:: shell

    SINGULARITY_NOHTTPS=1 singularity build $SINGULARITY_IMAGE docker://$DOCKER_REGISTRY_HOST:$DOCKER_REGISTRY_PORT/$DOCKER_IMAGE:$DOCKER_TAG

For example, to build a Singularity image called ``C-PAC-example.simg`` from the Docker image ``fcpindi/c-pac:example``:

.. code-block:: shell

    docker run -d -p 5000:5000 --restart=always --name registry registry:2
    docker tag fcpindi/c-pac:example localhost:5000/fcpindi/c-pac:example
    docker push localhost:5000/fcpindi/c-pac:example
    SINGULARITY_NOHTTPS=1 singularity build C-PAC-example.simg docker://localhost:5000/fcpindi/c-pac:example

.. 
    # From Dockerfile
    # ---------------
    # # This process seems to not be quite foolproof yet.
    #
    # `Singularity Python <https://singularityhub.github.io/singularity-cli/>`_ includes `a tool to convert a Dockerfile into a Singularity recipe <https://singularityhub.github.io//recipes#auto-detection>`_. Then you can build a Singularity image with that recipe. You'll need ``sudo`` permissions to build from a recipe. If your Singularity is installed somewhere outside of root's ``PATH``, you'll have to give the full path to the ``singularity`` executable file.
    #
    # .. code-block:: shell
    #
    #     spython recipe Dockerfile Singularity.snowflake
    #     sudo $SINGULARITY_PATH/singularity build $SINGULARITY_IMAGE Singularity.snowflake
    #
    #
    # For example, to build a Singularity image called ``C-PAC-example.simg`` from the Dockerfile:
    #
    # .. code-block:: shell
    #
    #     spython recipe Dockerfile Singularity.snowflake
    #     sudo ~/opt/singularity/singularity-2.5.2/bin/singularity build C-PAC-example.simg Singularity.snowflake
