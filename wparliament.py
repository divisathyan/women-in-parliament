#https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7

from flask import Flask, render_template, request, send_file
#from StringIO import StringIO
from pygal.style import LightColorizedStyle, RotateStyle
import pygal
import pygal_maps_world
from pygal.maps.world import World
import logging
import json

app = Flask(__name__)
app.config["DEBUG"] = True
@app.route('/', methods=['get'])
def index():
    logging.info("GET request path /")
    return render_template('index.html')

@app.route('/rendermap', methods=['post'])
def rendermap():
    message = ''
    result=''
    leaderitems={}
    cc=''
    logging.info("POST request path /rendermap")
    if request.method == 'POST':
        cc = request.form.get('countryCode')
        if cc == '':
            message = "Please enter a 2 letter ISO country code"
        cc = cc.lower()
        ccupper = cc.upper()
        logging.info("ISO country code entered:" + cc)
        
        #Load the country json
        with open('data/leaders.json') as leaders_json_file:
            leadersdata = json.load(leaders_json_file)
            #for w in leadersdata:
            #    print("%s: %d" % (w, leadersdata[w]))
            if ccupper not in leadersdata:
                message = "Wrong country code. Click Home link and enter a valid 2-letter ISO code!"
            else:
                leaderitems[cc]= float(leadersdata[ccupper])
                result= cc +":"+ str(leadersdata[ccupper])
                with open('data/neighbours.json') as neighbours_json_file:
                    nd = json.load(neighbours_json_file)
                    #for n in nd:
                    #    print("%s: %s" % (n, str(nd[n])))
                    narr = nd[cc]
                    for neighbour in narr:
                        nupper = neighbour.upper()
                        if nupper in leadersdata:
                            leaderitems[neighbour]= float(leadersdata[nupper])
                            result+= "," + str(neighbour) + ":" + str(leadersdata[nupper])
                        else:
                            message+= "Data not available for neighbouring country ISO Code:" + str(neighbour) + "\n"
                
                #Create world map with result
                wm_style = RotateStyle('#34126000')
                wm = World()
                wm.force_uri_protocol = 'http'

                wm.title="Women Political leaders (%)"
                wm.add('',leaderitems)
                wm.render_to_file('templates/lmap.svg')
                svg = render_template('lmap.svg')


    print("Result " + result)
    print("Message " + message)
    print(len(leaderitems))
    #svgf = open("templates/lmap.svg", "r").read()
    #svg_io = StringIO()
    #svg_io.write(svgf)
    #svg_io.seek(0)
    #return send_file(svg_io, mimetype='image/svg+xml')
    img = './static/lmap.svg'

    return render_template('leadersmap.html',message=message,img=img)

app.run()

