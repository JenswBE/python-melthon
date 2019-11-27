=======
Publish
=======
This document lists the steps required to publish a new version.

1. Run all tests with::

    tox

2. Update CHANGELOG.rst

3. Commit and push changes

4. Bump version with::

    bumpversion patch/minor/major

5. Clean build folder with::

    rm -rf build
    rm -rf src/*.egg-info

6. Build project::

    python3 setup.py clean --all sdist bdist_wheel

7. Upload to PyPI with::

    twine upload --skip-existing dist/*.whl dist/*.gz

8. Create Release on Git
