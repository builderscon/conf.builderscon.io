import bottle
import babel.support
import jinja2
import functools

DEBUG=False
TEMPLATES={}

""" This class adds support for i18n/l10n on top of the base bottle.Jinja2Template """
class Jinja2Template(bottle.Jinja2Template):
    def prepare(self, languages=['en_US'], filters=None, tests=None, globals={}, **kwargs):
        if 'prefix' in kwargs: # TODO: to be removed after a while
            raise RuntimeError('The keyword argument `prefix` has been removed. '
                'Use the full jinja2 environment name line_statement_prefix instead.')
        env = jinja2.Environment(loader=jinja2.FunctionLoader(self.loader), **kwargs)
        translations = babel.support.Translations.load('translations', languages)
        env.install_gettext_translations(translations)
        self.env = env
        if filters: self.env.filters.update(filters)
        if tests: self.env.tests.update(tests)
        if globals: self.env.globals.update(globals)
        if self.source:
            self.tpl = self.env.from_string(self.source)
        else:
            self.tpl = self.env.get_template(self.filename)

def template(*args, **kwargs):
    tpl = args[0] if args else None
    adapter = kwargs.pop('template_adapter', bottle.SimpleTemplate)
    lookup = kwargs.pop('template_lookup', bottle.TEMPLATE_PATH)
    languages = kwargs.pop('languages', None)
    tplid = (id(languages), tpl,)
    if tplid not in TEMPLATES or DEBUG:
        settings = kwargs.pop('template_settings', {})
        if languages: settings.update({'languages': languages})    
        if isinstance(tpl, adapter):
            TEMPLATES[tplid] = tpl
            if settings: TEMPLATES[tplid].prepare(**settings)
        elif "\n" in tpl or "{" in tpl or "%" in tpl or '$' in tpl:
            TEMPLATES[tplid] = adapter(source=tpl, lookup=lookup, **settings)
        else:
            TEMPLATES[tplid] = adapter(name=tpl, lookup=lookup, **settings)
    if not TEMPLATES[tplid]:
        abort(500, 'Template (%s) not found' % tpl)
    for dictarg in args[1:]: kwargs.update(dictarg)

    return TEMPLATES[tplid].render(kwargs)

template_settings = {
    'extensions': ['jinja2.ext.i18n']
}

jinja2_template = functools.partial(template, 
                            template_adapter=Jinja2Template,
                            template_settings=template_settings)
