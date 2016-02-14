django-switch-templatetag
=========================

A simple "switch" statement for Django templates.

Installation
------------

 * Install to PYTHONPATH, etc.

Then either:

 * Add ``switch_templatetag`` to ``settings.INSTALLED_APPS`` and then use::

     {% load switch_templatetag %}

   ... in your templates.

Or:

 * Add ``switch_templatetag.templatetags.switch`` to your
   ``BUILTINS`` entry in ``settings.TEMPLATES`` (Django 1.9)

Or:

 * Add to builtins (< Django 1.9) with in some ``models.py``::

     from django.template.base import add_to_builtins
     add_to_builtins('switch_templatetag.templatetags.switch'
