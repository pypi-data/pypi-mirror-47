# Django Simple DB Storage

A very simple app implementing the Django storages API, storing files in a database. A very simple view is provided for downloading files.

## Getting Started

1. Install the django-simpledbstorage pip package
2. Add the app to your project's INSTALLED_APPS, and urls
3. Set DEFAULT_FILE_STORAGE to 'simpledbstorage.storage.DatabaseStorage'
4. Set your MEDIA_URL, if relevant to you

## Example

In settings.py:
```python
DEFAULT_FILE_STORAGE = 'simpledbstorage.storage.DatabaseStorage'
INSTALLED_APPS.append('simpledbstorage')
MEDIA_URL = '/{}{}/'.format(BASE_PATH, 'files/')
```

In urls.py or wherever your URLconf lives:
```python
urlpatterns = [
  url(r'^files/', include('simpledbstorage.urls'))
]
```

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/SearchLightNZ/django-simpledbstorage/tags).
