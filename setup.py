from setuptools import setup, find_packages

setup(name='sbo_validate_email',
      version = '1.03',
      download_url = 'git@github.com:sefagerberg/sbo_validate_email.git',
      py_modules = ('sbo_validate_email',),
      author = 'Evan Fagerberg',
      author_email = 'efagerberg@safaribooksonline.com',
      description = 'validate_email verifies if an email address is valid and really exists.',
      long_description=open('README.rst').read(),
      keywords = 'email validation verification mx verify',
      url = 'http://github.com/efagerberg/sbo_validate_email',
      license = 'LGPL',
    )
