import os
import uuid
from django.db import models
from django.utils.deconstruct import deconstructible

@deconstructible
class UniqueWebpPath(object):
    def __init__(self, folder=None):
        self.folder = folder 

    def __call__(self, instance, filename):
        if instance is not None and hasattr(instance, '_meta'):
            folder_name = instance._meta.model_name + '_images'
        else:
            folder_name = self.folder or 'default_images'
        ext = 'webp'
        unique_name = f'{uuid.uuid4().hex}.{ext}'
        return os.path.join(folder_name, unique_name)