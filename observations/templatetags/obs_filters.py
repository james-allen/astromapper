import json

from django import template

register = template.Library()

@register.filter
def jsonify_exposure_list(exposure_list):
    exposure_json = json.dumps(
        [{'ra':e.ra, 'dec':e.dec, 'exposed':e.exposed, 
          'instrument_name':e.night.instrument.name} for e in exposure_list])
    return exposure_json
