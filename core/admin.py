from django.contrib import admin
from core.models import Url

# Register your models here.
class UrlAdmin(admin.ModelAdmin):
    #fields = ("fqdn", "queriedAt", "uuid", "dns" )
    list_display = ("fqdn", "queriedAt", "uuid")

admin.site.register(Url, UrlAdmin)