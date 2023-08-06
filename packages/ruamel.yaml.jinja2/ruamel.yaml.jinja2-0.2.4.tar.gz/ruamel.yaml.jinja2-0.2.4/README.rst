
ruamel.yaml.jinja2
==================

jinja2 templates for YAML files can normally not be loaded as YAML before 
rendering. This plugin allows pre and post-processing based on the
round-trip processor.

ChangeLog
=========

.. should insert NEXT: at the beginning of line for next key

0.2.4:
  - fix spurious .pth file for nested package.

0.2.3:
  - handling jinja2 comments, PR supplied by 
    `Jude N <https://bitbucket.org/%7Bf205c5b0-ee70-49f2-93d9-3c4ab10b935a%7D/>`__

0.2.2 (2017-10-11):
  - fix for Python 3.x

0.2.1 (2017-06-23):
  - add univeral wheel

0.2.0 (2017-06-23):
  - rename to __plug_in__.py

0.1.3 (2017-06-18):
  - remove generation of non-functional jinja2 executable

0.1.2 (2017-06-16):
  - added keyword, dependency on ruamel.yaml

0.1.1 (2017-06-14):
  - initial plug-in version

