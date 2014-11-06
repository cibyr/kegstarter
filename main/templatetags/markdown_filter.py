import bleach
import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()

ALLOWED_TAGS = [
    'a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code', 'col', 'colgroup',
    'del', 'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img', 'li',
    'ol', 'p', 'pre', 'strike', 'strong', 'sub', 'ul', 'table', 'tbody', 'td',
    'tfoot', 'th', 'thead', 'tr',
]

ALLOWED_ATTRIBUTES = {
    'a': ['href', 'title'],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['src', 'alt']
}

@register.filter(is_safe=True)
@stringfilter
def format_markdown(value):
    return mark_safe(bleach.linkify(bleach.clean(markdown.markdown(force_unicode(value),
                                                                   extensions=['markdown.extensions.sane_lists'],
                                                                   output_format='html5',
                                                                   lazy_ol=False),
                                                 tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES)))
