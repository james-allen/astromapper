from django.contrib import admin
from observations.models import Telescope, Instrument, Night, Exposure

class TelescopeAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude')
    search_fields = ['name']

class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'telescope')
    list_filter = ['telescope__name']
    search_fields = ['name', 'telescope__name']

class ExposureInline(admin.TabularInline):
    model = Exposure

class NightAdmin(admin.ModelAdmin):
    list_display = ('instrument', 'ut_date')
    list_filter = [
        'instrument__telescope__name', 'instrument__name', 'ut_date']
    inlines = [ExposureInline]
    search_fields = ['instrument__name']

class ExposureAdmin(admin.ModelAdmin):
    list_display = (
        'night', 'run_number', 'ra', 'dec', 'ut_start', 'object_exp')
    list_filter = [
        'night__instrument__name', 'night__ut_date', 'object_exp']
    search_fields = ['instrument__name']

admin.site.register(Telescope, TelescopeAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(Night, NightAdmin)
admin.site.register(Exposure, ExposureAdmin)
