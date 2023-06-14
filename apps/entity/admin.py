from django.contrib import admin
from .models import Entity, DirectoratePosition, Directorate, YearlyCensus, YearlyCensusEntry


class DirectoratePositionAdmin(admin.ModelAdmin):
    list_filter = ("entity",)
    list_display = ("entity", "name")

class DirectorateAdmin(admin.ModelAdmin):
    list_filter = ("entity",)
    list_display = ("entity", "position", "user")

admin.site.register(Entity)
admin.site.register(DirectoratePosition, DirectoratePositionAdmin)
admin.site.register(Directorate, DirectorateAdmin)
admin.site.register(YearlyCensus)
admin.site.register(YearlyCensusEntry)