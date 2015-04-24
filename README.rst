===================
sbo_validate_email
===================

sbo_validate_email is a package for Python that check if an email is valid, properly formatted and really exists.



INSTALLATION
============

First, you must do::

    pip install sbo_validate_email

Extra
------

For check the domain mx and verify email exits you must have the `pyDNS` package installed::

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

