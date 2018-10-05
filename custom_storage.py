# pylint: disable=W0223
""" contains the settings for the azure storage backend """
from django.conf import settings
from storages.backends.azure_storage import AzureStorage

class MediaStorage(AzureStorage):
    """ name of the azure_container for media files """
    azure_container = settings.MEDIAFILES_LOCATION

class StaticStorage(AzureStorage):
    """ name of the azure_container for static files """
    azure_container = 'static'
