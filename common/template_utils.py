import jinja2
import jinja2.ext
from .i18n import _
from . import utils
from . import jsonutils

if utils.IS_DJANGO_APP:
	from django.conf import settings
	from django.core.urlresolvers import reverse
	_static_url = settings.STATIC_URL
elif utils.IS_FLASK_APP:
	_static_url = utils.get_config().get('STATIC_URL', '')

if not _static_url:
	_static_url = './'
elif not _static_url.endswith('/'):
	_static_url += '/'

class StaticExtension(jinja2.ext.Extension):

	tags = set(['static'])

	def parse(self, parser):
		lineno = parser.stream.next().lineno
		args = [parser.parse_expression()]
		return jinja2.nodes.Output([self.call_method("_static", args=args)]).set_lineno(lineno)

	def _static(self, url):
		if url.startswith('/'):
			return _static_url + url[1:]
		else:
			return _static_url + url

class I18nExtension(jinja2.ext.Extension):

	tags = set(['_', 't'])

	def parse(self, parser):
		lineno = parser.stream.next().lineno
		args = [parser.parse_expression()]
		if parser.stream.skip_if('comma'):
			args.append(parser.parse_expression())
		else:
			args.append(jinja2.nodes.Name('language', 'load'))
		return jinja2.nodes.Output([self.call_method("_translate", args=args)]).set_lineno(lineno)

	def _translate(self, key, language):
		return _(key, language)

class UrlExtension(jinja2.ext.Extension):

	tags = set(['url'])

	def parse(self, parser):
		lineno = parser.stream.next().lineno
		method_args = [parser.parse_expression()]

		if parser.stream.skip_if('comma'):
			method_args.append(parser.parse_expression())
			if parser.stream.skip_if('comma'):
				method_args.append(parser.parse_expression())
		return jinja2.nodes.Output([self.call_method("_url", args=method_args)]).set_lineno(lineno)

	def _url(self, name, args=None, kwargs=None):
		return reverse(name, args=args, kwargs=kwargs)

_js_escapes = {
	ord('\\'): '\\u005C',
	ord('\''): '\\u0027',
	ord('"'): '\\u0022',
	ord('>'): '\\u003E',
	ord('<'): '\\u003C',
	ord('&'): '\\u0026',
	ord('='): '\\u003D',
	ord('-'): '\\u002D',
	ord(';'): '\\u003B',
	ord('\u2028'): '\\u2028',
	ord('\u2029'): '\\u2029'
}

# Escape every ASCII character with a value less than 32.
_js_escapes.update((ord('%c' % z), '\\u%04X' % z) for z in range(32))

def escape_js_string(s):
	if isinstance(s, str):
		s = s.decode('utf-8')
	return s.translate(_js_escapes)

def escapejs_filter(s):
	return jinja2.Markup(escape_js_string(s))

@jinja2.contextfilter
def translate_filter(ctx, key, language=None):
	if language is None:
		language = ctx.get('language', None)
	return _(key, language)

if utils.IS_DJANGO_APP:

	from django.http import HttpResponse
	from django.template import RequestContext

	def tojson(data):
		if isinstance(data, jinja2.runtime.Undefined):
			return 'null'
		return jinja2.Markup(jsonutils.to_json_html_safe(data))

	def autoescape_for_xml(filename):
		if filename is None:
			return False
		return filename.endswith(('.html', '.htm', '.xml', '.xhtml'))

	env = jinja2.Environment(loader=jinja2.PackageLoader(settings.APP_NAME, 'templates'),
							autoescape=autoescape_for_xml, extensions=[StaticExtension, I18nExtension, UrlExtension])
	env.filters['escapejs'] = escapejs_filter
	env.filters['tojson'] = tojson
	env.filters['t'] = translate_filter
	env.filters['_'] = translate_filter

	def template_render(template_name, *args, **kwargs):
		"""
		Returns the text rendered by the jinja2 engine.
		Adds Django template context processor support.
		"""
		context = {}
		if 'context_instance' in kwargs:
			context_instance = kwargs.pop('context_instance')
			for d in context_instance.dicts:
				context.update(d)
		context.update(*args, **kwargs)
		return env.get_template(template_name).render(context)

	def render_to_response(template_name, *args, **kwargs):
		"""
		Returns a HttpResponse whose content is filled with the result of calling
		jinja2 template render with the passed arguments.
		"""
		httpresponse_kwargs = {'content_type': kwargs.pop('content_type', None)}
		return HttpResponse(template_render(template_name, *args, **kwargs), **httpresponse_kwargs)

	def render(request, template_name, *args, **kwargs):
		"""
		Returns a HttpResponse whose content is filled with the result of calling
		jinja2 template render with the passed arguments.
		Uses a RequestContext by default.
		"""
		httpresponse_kwargs = {
			'content_type': kwargs.pop('content_type', None),
			'status': kwargs.pop('status', None),
		}

		if 'context_instance' in kwargs:
			context_instance = kwargs.pop('context_instance')
			if kwargs.get('current_app', None):
				raise ValueError('If you provide a context_instance you must '
								 'set its current_app before calling render()')
		else:
			current_app = kwargs.pop('current_app', None)
			context_instance = RequestContext(request, current_app=current_app)

		kwargs['context_instance'] = context_instance

		return HttpResponse(template_render(template_name, *args, **kwargs),
							**httpresponse_kwargs)

elif  utils.IS_FLASK_APP:

	from flask import Response
	import flask

	env = utils.get_app().jinja_env
	env.add_extension(StaticExtension)
	env.add_extension(I18nExtension)
	env.filters['escapejs'] = escapejs_filter
	env.filters['t'] = translate_filter
	env.filters['_'] = translate_filter

	def template_render(template_name, *args, **kwargs):
		context = {}
		if 'context_instance' in kwargs:
			context_instance = kwargs.pop('context_instance')
			for d in context_instance.dicts:
				context.update(d)
		context.update(*args, **kwargs)
		return flask.render_template(template_name, **context)

	def render_to_response(template_name, *args, **kwargs):
		httpresponse_kwargs = {'content_type': kwargs.pop('content_type', None)}
		return Response(template_render(template_name, *args, **kwargs), **httpresponse_kwargs)
