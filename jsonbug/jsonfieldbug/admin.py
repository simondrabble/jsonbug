from django.contrib import admin

from . import models


admin.site.register(models.JsonSerializationBug, admin.ModelAdmin)
