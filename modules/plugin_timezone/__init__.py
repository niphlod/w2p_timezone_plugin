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
      ('Etc/GMT+12',                    '(UTC-12:00) International Date Line West'),
      ('Pacific/Majuro',                '(UTC+12:00) Coordinated Universal Time+12'),
      ('Pacific/Pago_Pago',             '(UTC-11:00) Coordinated Universal Time-11'),
      ('America/Adak',                  '(UTC-09:00) Adak'),
      ('Pacific/Honolulu',              '(UTC-10:00) Hawaii'),
      ('Pacific/Marquesas',             '(UTC-09:30) Marquesas'),
      ('Pacific/Gambier',               '(UTC-09:00) Gambier'),
      ('America/Anchorage',             '(UTC-09:00) Alaska'),
      ('America/Los_Angeles',           '(UTC-08:00) Pacific Time (US & Canada)'),
      ('Pacific/Pitcairn',              '(UTC-08:00) Pitcairn'),
      ('America/Phoenix',               '(UTC-07:00) Arizona'),
      ('America/Chihuahua',             '(UTC-07:00) Chihuahua, La Paz, Mazatlan'),
      ('America/Denver',                '(UTC-07:00) Mountain Time (US & Canada)'),
      ('America/Guatemala',             '(UTC-06:00) Central America'),
      ('America/Chicago',               '(UTC-06:00) Central Time (US & Canada)'),
      ('Pacific/Easter',                '(UTC-05:00) Estearn Pacific'),
      ('America/Bogota',                '(UTC-05:00) Bogota, Lima, Quito'),
      ('America/New_York',              '(UTC-05:00) Eastern Time (US & Canada)'),
      ('America/Caracas',               '(UTC-04:30) Caracas'),
      ('America/Halifax',               '(UTC-04:00) Atlantic Time (Canada)'),
      ('America/Santo_Domingo',         '(UTC-04:00) Georgetown, La Paz, Manaus, San Juan'),
      ('America/Santiago',              '(UTC-04:00) Santiago'),
      ('America/St_Johns',              '(UTC-03:30) Newfoundland'),
      ('America/Sao_Paulo',             '(UTC-03:00) Brasilia'),
      ('America/Argentina/Buenos_Aires','(UTC-03:00) Buenos Aires'),
      ('America/Cayenne',               '(UTC-03:00) Cayenne, Fortaleza'),
      ('America/Godthab',               '(UTC-03:00) Greenland'),
      ('America/Montevideo',            '(UTC-03:00) Montevideo'),
      ('America/Bahia',                 '(UTC-03:00) Salvador'),
      ('America/Noronha',               '(UTC-02:00) Coordinated Universal Time-02'),
      ('Atlantic/Azores',               '(UTC-01:00) Azores'),
      ('Atlantic/Cape_Verde',           '(UTC-01:00) Cape Verde Is.'),
      ('UTC',                           '(UTC) Coordinated Universal Time'),
      ('Europe/London',                 '(UTC) Dublin, Edinburgh, Lisbon, London'),
      ('Europe/Berlin',                 '(UTC+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna'),
      ('Africa/Lagos',                  '(UTC+01:00) West Central Africa'),
      ('Africa/Windhoek',               '(UTC+01:00) Windhoek'),
      ('Europe/Bucharest',              '(UTC+02:00) Athens, Bucharest'),
      ('Asia/Beirut',                   '(UTC+02:00) Beirut'),
      ('Africa/Johannesburg',           '(UTC+02:00) Harare, Pretoria'),
      ('Asia/Baghdad',                  '(UTC+03:00) Baghdad'),
      ('Africa/Nairobi',                '(UTC+03:00) Nairobi'),
      ('Europe/Moscow',                 '(UTC+04:00) Moscow, St. Petersburg, Volgograd'),
      ('Asia/Tehran',                   '(UTC+03:30) Tehran'),
      ('Asia/Dubai',                    '(UTC+04:00) Abu Dhabi, Muscat'),
      ('Asia/Baku',                     '(UTC+04:00) Baku'),
      ('Asia/Kabul',                    '(UTC+04:30) Kabul'),
      ('Asia/Yekaterinburg',            '(UTC+06:00) Ekaterinburg'),
      ('Asia/Karachi',                  '(UTC+05:00) Islamabad, Karachi'),
      ('Asia/Kolkata',                  '(UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi'),
      ('Asia/Kathmandu',                '(UTC+05:45) Kathmandu'),
      ('Asia/Dhaka',                    '(UTC+06:00) Dhaka'),
      ('Asia/Omsk',                     '(UTC+07:00) Novosibirsk'),
      ('Asia/Rangoon',                  '(UTC+06:30) Yangon (Rangoon)'),
      ('Asia/Krasnoyarsk',              '(UTC+08:00) Krasnoyarsk'),
      ('Asia/Jakarta',                  '(UTC+07:00) Bangkok, Hanoi, Jakarta'),
      ('Asia/Shanghai',                 '(UTC+08:00) Beijing, Chongqing, Hong Kong, Urumqi'),
      ('Asia/Irkutsk',                  '(UTC+09:00) Irkutsk'),
      ('Australia/Eucla',               '(UTC+08:45) Eucla'),
      ('Asia/Yakutsk',                  '(UTC+10:00) Yakutsk'),
      ('Asia/Tokyo',                    '(UTC+09:00) Osaka, Sapporo, Tokyo'),
      ('Australia/Darwin',              '(UTC+09:30) Darwin'),
      ('Australia/Adelaide',            '(UTC+09:30) Adelaide'),
      ('Australia/Brisbane',            '(UTC+10:00) Brisbane'),
      ('Asia/Vladivostok',              '(UTC+11:00) Vladivostok'),
      ('Australia/Sydney',              '(UTC+10:00) Canberra, Melbourne, Sydney'),
      ('Australia/Lord_Howe',           '(UTC+10:30) Lord_Howe'),
      ('Pacific/Noumea',                '(UTC+11:00) Solomon Is., New Caledonia'),
      ('Pacific/Norfolk',               '(UTC+11:30) Norfolk'),
      ('Asia/Kamchatka',                '(UTC+12:00) Magadan'),
      ('Pacific/Auckland',              '(UTC+12:00) Auckland, Wellington'),
      ('Pacific/Tarawa',                '(UTC+12:00) Coordinated Universal Time+12'),
      ('Pacific/Chatham',               '(UTC+12:45) Chatam'),
      ('Pacific/Tongatapu',             '(UTC+13:00) Nuku\'alofa'),
      ('Pacific/Apia',                  '(UTC+13:00) Samoa'),
      ('Pacific/Kiritimati',            '(UTC+14:00) Kiritimati')
]

def tz_nice_detector_widget(field, value, **attributes):
    nice_TZSETS = []
    for tzn in TZSETS:
        #retrieve offset
        localized = datetime.datetime.now(pytz.timezone(tzn[0]))
        nice_TZSETS.append((tzn[0], tzn[1], localized.strftime('%Y-%m-%d %H:%M')))

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
