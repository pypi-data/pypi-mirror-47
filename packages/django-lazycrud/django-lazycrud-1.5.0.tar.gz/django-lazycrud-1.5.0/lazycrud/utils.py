import types
from datetime import datetime, date

from django.utils import formats
from django.utils.timezone import localtime

def formatDate(dt):
    if dt is None:
        return 'n.d.'
    return formats.date_format(dt, "SHORT_DATE_FORMAT")

def formatDateTime(dt):
    if dt is None:
        return 'n.d.'
    return formats.date_format(localtime(dt), "SHORT_DATETIME_FORMAT")

def fieldlabel(obj, key):
    try:
        return obj._meta.get_field(key).verbose_name.strip().capitalize() # strip serve per forzare l'esecuzione di ugettext_lazy
    except:
        try:
            return getattr(obj, '%s_label' % key)()
        except:
            return key.capitalize().replace('_', ' ')

def fieldvalue(obj, key):
    try:
        return getattr(obj, 'get_%s_display' % key)()
    except:
        try:
            ret = getattr(obj, key)
        except:
            ret = None
        if type(ret) == types.MethodType:
            ret = ret()
        if ret is None:
            ret = ''
        elif isinstance(ret, datetime):
            ret = formatDateTime(ret)
        elif isinstance(ret, date):
            ret = formatDate(ret)
        return ret
