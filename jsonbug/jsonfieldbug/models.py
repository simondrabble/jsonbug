from django.db import models


from jsonfield import JSONField


class JsonSerializationBug(models.Model):

    data = JSONField(unique=True)
