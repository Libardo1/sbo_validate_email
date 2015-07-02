===================
sbo_validate_email
===================

sbo_validate_email is a package for Python that check if an email is valid, properly formatted and really exists.


Dependency
==========

For checking the domain mx and verifying email exits you must have the `pyDNS` package installed::

    pip install pyDNS


USAGE
=====

Basic usage::

    from sbo_validate_email import validate_email
    is_valid = validate_email('example@example.com')


Checking domain has mx record
-------------------------------

Check if the host has SMTP Server::

    from validate_email import validate_email
    is_valid = validate_email('example@example.com',check_mx=True)


Releasing a new egg
===================

To upload a new nest egg to our internal PyPI repository (after you've incremented the version number and updated the changelog file):


$ python setup.py sdist upload -r internal


More information and setup steps can be found :doc:`here <internal-pypi>`.
