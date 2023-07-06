# django-one-time-notices

Displays a modal with notice content if a user hasn't seen it yet.

## Install
```
pip install django-one-time-notices
```

## Settings

Add to `INSTALLED_APPS`:

```
django.contrib.auth
django.contrib.admin
...
notices
```


Add to `TEMPLATES['OPTIONS']`:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                ...
                'django.core.context_processors.request'
                ...
                'notices.context_processors.notices',
            ]
        }
    }
]
```             

To customise the notice colour (button and title border), add
```
NOTICES_COLOUR=<colour>  # any css-acceptable colour
```

## Static assets
Add `notices/css/notices.css` and `notices/js/notices.js` to your markup.

## Usage
In templates, load the tags:
```
{% load notices_tags %}
```

and add the modal:
```
{% NoticesModal %} 
```

The modal will be shown.  Once it has been dismissed it won't be shown again unless the notice version changes (see below), the `notice_seen` cookie is deleted, or the notice timeout is reached.

## Setting/updating the notice

### via models and django admin
Add a `Notice` instance in the django admin. 

Notices have `title`, `content`, `version` and optional `timeout_seconds`, `starts_at` and `expires_at` fields.

Version can be any positive number; it defaults to incrementing the last version number.  Set the `expires_at` datetime to avoid showing this notice after the specified date, even if the user has never seen/dismissed it. Set the `starts_at` datetime to avoid showing the notice until a
particular date/time.

Note that only the notice with the latest version will be shown. If the latest version
has not started yet, a previous version will not be shown, even if it hasn't expired. 

Set the `timeout_seconds` to set a cookie timeout; this means the notice will be reshown.

To show a new notice, add another Notice instance with an incremented version number.

### via django settings

Override the Notice model by adding to your `settings.py`:
`NOTICES_VERSION` # an integer
`NOTICES_TITLE`  # optional, default = "New!"
`NOTICES_CONTENT`  # optional, default = ""
`NOTICES_TIMEOUT_SECONDS`  # optional, default = None

Set `NOTICES_VERSION = 0` to clear the cookie and disable showing notices at all.
