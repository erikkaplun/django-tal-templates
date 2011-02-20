Django TAL Templates
====================

Requirements
------------

* Django 1.2
* Chameleon

Installation
------------

* Make sure the ``tal_templates`` directory is in your
  ``sys.path``/``PYTHONPATH``
* Add ``'tal_templates.loaders.Loader'`` to ``TEMPLATE_LOADERS``

Introduction
------------

This package adds TAL templates support to Django using Chameleon. It
provides a custom template loader and a Template class. The loader
simply inherits from the Django standard app directories template
loader.

In addition to rendering template files using the Zope TAL
templating language (using Chameleon), the templates are first rendered
using the built in Django templating language. This enables mixing
of Django template code and TAL. This is to provide more flexibility
and a more gradual migration.


Motivation
----------

The Django template language does not streamline well with the structure
of XML based markup languages such as HTML. This often causes
duplication and readability issues. For example, the following exmple
block demonstrates how a single ``{% for %}`` tag duplicates structure
that already exists in HTML::

    <ul>
        {% for post in posts %}
        <li><a href="{{ post.url }}">{{ post.title }}</a></li>
        {% endfor %}
    </ul>

The ``{% for ... %}`` and ``{% endfor %}`` pair duplicates the structure
already defined by the ``<ul>`` and ``</ul>`` pair. TAL provides a
solution to this::

    <ul>
        <li tal:repeat="post posts"><a href="${post.url}">${post.title}</a></li>
    </ul>


Caveats
-------

It is not possible to access variables dynamically created by Django
from TAL code, and vice versa. The following examples do not work as
might be expected.

Accessing a variable created by Django from TAL::

    {% with foo=article.get_foo }}
    ${foo}
    {% endiwth %}


Accessing a variable created by TAL from a Django block::

    <div tal:repeat="post posts">
        {{ post.title }}
    </div>

The reason for this is that the templating engines are run
sequentially. Even if it were possible for TAL to access
variables created by Django, by the time TAL execution begins,
the Django templating engine would have already finished, together
with any variables it created. The opposite would be even more
absurd because TAL runs after Django.

However, the context passed in from the view can be accessed by both
equally well.


Missing features
----------------

Currently, the template loader provided by this package inherits from
``django.template.loaders.app_directories.Loader`` which means that only
templates contained in app template directories have access to TAL.
