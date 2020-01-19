=======
Publish
=======
This document lists the steps required to publish a new version.

1. Install requirements (on Ubuntu)::

    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.5 python3.6 python3.7 python3.8
    sudo snap install --classic pypy3
    pip3 install tox

2. Run all tests with::

    tox

3. Update CHANGELOG.rst

4. Commit and push changes

5. Bump version with::

    bumpversion patch/minor/major

6. Clean build folder with::

    rm -rf build
    rm -rf src/*.egg-info

7. Build project::

    python3 setup.py clean --all sdist bdist_wheel

8. Upload to PyPI with::

    twine upload --skip-existing dist/*.whl dist/*.gz

9. Create Release on Git
