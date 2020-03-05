import pygal
import pygal_maps_world
#import base64
from pygal.maps.world import World
#from ipywidgets import HTML
from flask import Flask
from flask import request

print("1")
if request.method == 'POST':
    print("1")
    countryCode = request.form['code']
else:
    print('No country code entered!')

wm = World()
wm.force_uri_protocol = 'http'

wm.title="Women Political leader distribution across countries"
wm.add('Leaders',{'ca': 4,'mx': 1,'us': 6})
#wm.chart.render()
wm.render_to_file('map.svg')
#b64 = base64.b64encode(wm.render())
#src = 'data:image/svg+xml;charset=utf-8;base64,'+b64
#HTML('<embed src={}></embed>'.format(src))