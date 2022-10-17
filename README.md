# django-notices

Displays a modal with notice content if a user hasn't seen it yet.

## Settings

Add `notices` to `INSTALLED_APPS` 

`NOTICES_TITLE`: default "New!
`NOTICES_VERSION`: an integer, >= 1
`NOTICES_CONTENT`: The modal content. A string, use `\n` linebreaks if required.

Set `NOTICES_VERSION` to 0 to never show the modal.

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

## Updating the notices
When you have a new notice to display, update the `NOTICES_CONTENT` and increment the `NOTICES_VERSION` to display the new content and update the cookie again.

Use environment variables to load the `NOTICES_` settings to avoid having to change
code for updates.
