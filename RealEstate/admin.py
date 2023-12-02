from django.contrib import admin
from .models import OmahaEvent, Owner, PropertyPriceRange, PropertyType, PropertyNeighborhood, PropertyListing


class OmahaEventAdmin(admin.ModelAdmin):
    list_display = ('omaha_event_id', 'omaha_event_title', 'omaha_event_url', 'omaha_event_description', 'event_image')
    search_fields = ['omaha_event_title', 'omaha_event_description']


admin.site.register(Owner)

admin.site.register(PropertyType)

admin.site.register(OmahaEvent, OmahaEventAdmin)
admin.site.register(PropertyListing)
admin.site.register(PropertyNeighborhood)
admin.site.register(PropertyPriceRange)
