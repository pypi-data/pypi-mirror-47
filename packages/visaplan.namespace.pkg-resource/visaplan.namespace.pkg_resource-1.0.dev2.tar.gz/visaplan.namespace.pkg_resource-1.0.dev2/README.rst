.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===============================
visaplan.namespace.pkg_resource
===============================

This is a dummy package which does nothing except providing the `visaplan`
package and namespace package, "pkg_resource style";
it was a workaround for the problem of e.g. `visaplan.tools`_ being installable,
but under certain circumstances, the package namespace doesn't work, and the
visaplan.tools submodules
`couldn't be accessed from the buildout-generated Plone instance`_.

Since the problem was solved, the `visaplan.namespace.pkg_resource` package is considered obsolete.


Features
--------

- Provides an empty namespace package `visaplan`.


Installation
------------

Install the `visaplan` dummy package by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.namespace.pkg_resource
        visaplan.tools
        ...


and then running ``bin/buildout``


License
-------

The project is available under the Apache License 2.0 or the GNU GPL 2.0

.. _`visaplan.tools`: https://pypi.org/project/visaplan.tools
.. _`couldn't be accessed from the buildout-generated Plone instance`: https://community.plone.org/t/factoring-out-packages-namespace-problem/6842
