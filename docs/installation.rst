============
Installation
============

Preferred way is to use Docker::

    # --rm           : Remove container after execution
    # -u ${UID}      : Run container as current user
    # -v"$(pwd):/src": Make source and output accessible inside container
    docker run --rm -u ${UID} -v"$(pwd):/src" jenswbe/melthon

At the command line::

    pip install melthon
