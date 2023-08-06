=====
Usage
=====


To develop on mapscookiegettercli:

.. code-block:: bash

    # The following commands require pipenv as a dependency

    # To lint the project
    _CI/scripts/lint.py

    # To execute the testing
    _CI/scripts/test.py

    # To create a graph of the package and dependency tree
    _CI/scripts/graph.py

    # To build a package of the project under the directory "dist/"
    _CI/scripts/build.py

    # To see the package version
    _CI/scripts/tag.py

    # To bump semantic versioning [--major|--minor|--patch]
    _CI/scripts/tag.py --major|--minor|--patch

    # To upload the project to a pypi repo if user and password are properly provided
    _CI/scripts/upload.py

    # To build the documentation of the project
    _CI/scripts/document.py


To use mapscookiegettercli:

    # This tool is written for python3.7

.. code-block:: bash

    Follow installation procedure from INSTALLATION.srt for your appropriate toolset.


    # execute the tool
    maps-cookie-getter

    # After the full login process the browser should be terminated and a "location_sharing.cookies"
    # file should be located at the same location that can be provided to the locationsharinglib.
