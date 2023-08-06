.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

====================
visaplan.js.urlsplit
====================

This is a simple Zope / Plone integration of the `urlSplit.js`_ Javascript tool.

Features
--------

- Makes available both the comprssed and uncompressed versions of ``urlSplit.js``
- Adds the compressed version to the Javascript registry


Documentation
-------------

For the Javascript functonality, please see `urlSplit.js`.


Installation
------------

Install visaplan.js.urlsplit by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.js.urlsplit


and then running ``bin/buildout``


Contribute
----------

For the Javascript functionality, please contribute to `urlSplit.js`_.

For the Zope / Plone integration:

- Issue Tracker: https://github.com/collective/visaplan.js.urlsplit/issues
- Source Code: https://github.com/collective/visaplan.js.urlsplit
- Documentation: https://docs.plone.org/foo/bar


License
-------

The project is licensed under the MIT License.

.. _`urlSplit.js`: https://github.com/hans-sperling/urlSplit.js
