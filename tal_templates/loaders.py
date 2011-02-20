# coding: utf-8
import django.template
from django.template.loaders.app_directories import Loader as AppDirLoader
from chameleon.zpt.template import PageTemplate


__all__ = ['Template', 'Loader',]


class Template(object):
    """Template class to render templates first through the Django
    templating language and then Zope TAL via SimpleTAL.

    """

    def __init__(self, source):
        """Initializes this Template object using the template source
        string as the only argument.

        """
        self._source = source

    def render(self, context):
        """Renders the template using Django and TAL."""
        dj_output = self._render_django_tpl(context, self._source)
        tal_output = self._render_tal_tpl(context, dj_output)
        return tal_output

    def _render_django_tpl(self, context, source):
        django_tpl = django.template.Template(source)
        return django_tpl.render(context)

    def _render_tal_tpl(self, context, source):
        # Unintuitively, context.dicts DOES NOT contain dicts only.
        # If, for example, render_to_response is called like this:
        #
        #     render_to_response('tpl.html', RequestContext(request, {}))
        #
        # then that RequestContext instance ends up in context.dicts.
        # So we have to check each item in the context.dicts attribute
        # and recursively get its dicts if it's a Context object not
        # a dict.
        context_dict = {}
        def build_context_dict(dicts):
            for d in dicts:
                if isinstance(d, django.template.Context):
                    build_context_dict(d.dicts)
                else:
                    context_dict.update(d)
        build_context_dict(context.dicts)

        return PageTemplate(source).render(**context_dict)


class Loader(AppDirLoader):
    """A template loader that behaves exactly like the Django app
    directories template loader except the template objects returned
    render the template source first through the Django templating
    language and then Zope TAL.

    """

    def load_template(self, template_name, template_dirs=None):
        """Loads the template source like the Django app directories
        template loader, but returns a customized Template object.

        """

        source, origin = self.load_template_source(template_name, template_dirs)
        template = Template(source)
        return template, origin
