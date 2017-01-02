Timezone handling simplified for web2py
===================
Since 2.4.5 web2py ships with IS_DATE* validators that accept a timezone parameter.
This is nice 'cause you can transparently treat all dates in your backend as UTC and transform them back
and forth to the client.
This plugin offers:
- a nice integration (hopefully) with one of the most concise/precise javascript
libraries out there to auto-detect the user timezone (http://pellepim.bitbucket.org/jstz/)
- a widget helper to give a nice representation of available timezones

Back to web2py: how does it deal with timezones ?

```python
import pytz

db.define_table('sometable',
  Field('appointment', 'datetime', 
        requires=IS_DATETIME(timezone=pytz.timezone("America/Chicago"))
  )
)
```

expanding a bit on having something session dependant

```python
import pytz
user_timezone = session.timezone or 'UTC'

db.define_table('sometable',
  Field('appointment', 'datetime', 
        requires=IS_DATETIME(timezone=pytz.timezone(user_timezone))
  )
)
```

So, back to the plugin ....
In one of your models, place

```python
import pytz
user_timezone = session.plugin_timezone_tz or 'UTC'

db.define_table('sometable',
  Field('appointment', 'datetime', 
        requires=IS_DATETIME(timezone=pytz.timezone(user_timezone))
  )
)
```

In a controller, place

```python
from plugin_timezone import fast_tz_detector
def detect_timezone():
    tz = fast_tz_detector()
    return dict(tz=tz)
```

As soon as you call this page, ```session.plugin_timezone_tz``` is filled automatically
with the detected timezone. Date(times) in the table 'sometable' are now automatically stored as UTC
and translated back to the user timezone when displayed in a form (or, in SQLFORM.grid)

Let's say you want instead to let the user choose its preferred timezone, and make it
a Field of the 'auth_user' table....
In your db.py, place 

```python
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()
.....
from plugin_timezone import tz_nice_detector_widget

auth.settings.extra_fields['auth_user']= [
  Field('user_timezone', 'string', widget=tz_nice_detector_widget),
]

auth.define_tables(username=False, signature=False)
```

Now, go to the Register page (or the Profile one), to see it ...
Take it to a step further: we show to the user the dropdown, but we also
auto-detect the timezone the user is in ....

```python
auth = Auth(db)
crud, service, plugins = Crud(db), Service(), PluginManager()
.....
from plugin_timezone import tz_nice_detector_widget
my_tz_nice_detector_widget = lambda field, value : tz_nice_detector_widget(field, value, autodetect=True)

auth.settings.extra_fields['auth_user']= [
  Field('user_timezone', 'string', widget=my_tz_nice_detector_widget),
]

auth.define_tables(username=False, signature=False)
```
Try and see for yourself!!!
With the preferred timezone set into the auth_user table, you can now change a bit your 'sometable'
definition

```python
import pytz
user_timezone = auth.user.user_timezone or 'UTC'

db.define_table('sometable',
  Field('appointment', 'datetime', 
        requires=IS_DATETIME(timezone=pytz.timezone(user_timezone))
  )
)
```
And voilà, all done.


TODO : 
- [ ] Add more docs ?
- [ ] Add tests ?
