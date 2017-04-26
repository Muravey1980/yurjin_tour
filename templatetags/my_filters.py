'''
Created on 2017-04-26
@author:   067SvobodskiiSE
@contact: ssvobodskii@067.pfr.ru
'''
from django import template
register = template.Library()


@register.filter(name='verbose_name')
def verbose_name(value):
    return value._meta.verbose_name
#register.filter('verbose_name', verbose_name)

@register.filter(name='verbose_name_plural')
def verbose_name_plural(value):
    return value._meta.verbose_name_plural
#register.filter('verbose_name_plural', verbose_name_plural)