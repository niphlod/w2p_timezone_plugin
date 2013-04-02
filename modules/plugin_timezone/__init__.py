try:
    import pytz
except:
    raise ImportError, 'You must install pytz'

import datetime

from gluon import current
from gluon.html import URL, OPTION, SELECT, SCRIPT, CAT
from gluon.sqlhtml import SQLFORM
from gluon.dal import Field

TZSETS = [
      'Pacific/Majuro',
      'Pacific/Pago_Pago',
      'America/Adak',
      'Pacific/Honolulu',
      'Pacific/Marquesas',
      'Pacific/Gambier',
      'America/Anchorage',
      'America/Los_Angeles',
      'Pacific/Pitcairn',
      'America/Phoenix',
      'America/Denver',
      'America/Guatemala',
      'America/Chicago',
      'Pacific/Easter',
      'America/Bogota',
      'America/New_York',
      'America/Caracas',
      'America/Halifax',
      'America/Santo_Domingo',
      'America/Santiago',
      'America/St_Johns',
      'America/Godthab',
      'America/Argentina/Buenos_Aires',
      'America/Montevideo',
      'America/Noronha',
      'America/Noronha',
      'Atlantic/Azores',
      'Atlantic/Cape_Verde',
      'UTC',
      'Europe/London',
      'Europe/Berlin',
      'Africa/Lagos',
      'Africa/Windhoek',
      'Asia/Beirut',
      'Africa/Johannesburg',
      'Asia/Baghdad',
      'Europe/Moscow',
      'Asia/Tehran',
      'Asia/Dubai',
      'Asia/Baku',
      'Asia/Kabul',
      'Asia/Yekaterinburg',
      'Asia/Karachi',
      'Asia/Kolkata',
      'Asia/Kathmandu',
      'Asia/Dhaka',
      'Asia/Omsk',
      'Asia/Rangoon',
      'Asia/Krasnoyarsk',
      'Asia/Jakarta',
      'Asia/Shanghai',
      'Asia/Irkutsk',
      'Australia/Eucla',
      'Australia/Eucla',
      'Asia/Yakutsk',
      'Asia/Tokyo',
      'Australia/Darwin',
      'Australia/Adelaide',
      'Australia/Brisbane',
      'Asia/Vladivostok',
      'Australia/Sydney',
      'Australia/Lord_Howe',
      'Asia/Kamchatka',
      'Pacific/Noumea',
      'Pacific/Norfolk',
      'Pacific/Auckland',
      'Pacific/Tarawa',
      'Pacific/Chatham',
      'Pacific/Tongatapu',
      'Pacific/Apia',
      'Pacific/Kiritimati'
]

def tz_nice_detector_widget(field, value, **attributes):
    nice_TZSETS = []
    for tzn in TZSETS:
        #retrieve offset
        localized = datetime.datetime.now(pytz.timezone(tzn))
        nice_TZSETS.append((tzn, "%s GMT%s" % (tzn, localized.strftime('%z')), localized.strftime('%Y-%m-%d %H:%M')))

    _id = '%s_%s' % (field._tablename, field.name)
    _name = field.name
    options = [OPTION(tzn[1], _value=tzn[0], data=dict(localized=tzn[2])) for tzn in nice_TZSETS]
    if 'autodetect' in attributes and attributes.pop('autodetect') is True:
        current.response.files.append(URL('static', 'plugin_timezone/jstz.min.js'))
        script = """
jQuery(document).ready(function () {
  var tz = jstz.determine();
  var nice_tz_select = jQuery('#%(_id)s');
  nice_tz_select.on('change.plugin_timezone', function(e, data) {
      var localized = jQuery('#%(_id)s option:selected').data('localized');
      var placeholder = '#plugin_timezone_localized';
      console.log('z', (!placeholder.length))
      if (!jQuery(placeholder).length) nice_tz_select.after('<span id="plugin_timezone_localized" style="display: block" />');
      if (typeof (data) !== 'undefined') {
        localized = 'auto: ' + localized;
      }
      else {
        manual = 'auto: ' + localized;
      }
      jQuery(placeholder).html(localized);
  });
  if (typeof (tz) !== 'undefined') {
      var name = tz.name();
      nice_tz_select.val(name).trigger('change.plugin_timezone', [name]);
  }
});
    """ % dict(_id=_id)
        return CAT(SELECT(*options, _id=_id, _name=_name, **attributes), SCRIPT(script))
    return SELECT(*options, _id=_id, _name=_name, **attributes)

def fast_tz_detector():
    current.response.files.append(URL('static', 'plugin_timezone/jstz.min.js'))
    ##//cdnjs.cloudflare.com/ajax/libs/jstimezonedetect/1.0.4/jstz.min.js
    script = """
jQuery(document).on('plugin_timezone.fast_tz_detector', function (e) {
    var tz = jstz.determine();
    if (typeof (tz) !== 'undefined') {
        var name = tz.name()
        jQuery.post('%s', {timezone : name});
    }
});
jQuery(document).ready(function () {
    jQuery(this).trigger('plugin_timezone.fast_tz_detector');
});
""" % URL()
    if current.request.post_vars.timezone:
        if current.request.post_vars.timezone in TZSETS:
            current.session.plugin_timezone_tz = current.request.post_vars.timezone
    return SCRIPT(script)
