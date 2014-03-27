#!/usr/bin/env python

# THE SOCIAL WEB 2014 -
# FINAL ASSIGNMENT
# CREATED BY: GROUP 31
# > Jeffery Bruijntjes: #jbs257
# > Marije ten brink: #mbk262
# > Jeroen Wever: #jwr970

#imports
import os
import aspire
import json
import cherrypy

VIEWS = os.path.join(os.path.abspath("."), u"views")

class Root:

    @cherrypy.expose
    def index(self):
        return open(os.path.join(VIEWS, u'discover.html'))

    @cherrypy.expose
    def compare(self):
        return open(os.path.join(VIEWS, u'compare.html'))

    @cherrypy.expose
    def aspirations(self, name):
        return json.dumps(aspire.start(name.lower()))

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    conf = {
        '/js': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(current_dir, 'js'),
            'tools.staticdir.content_types': {
                'js': 'application/x-javascript'
            }
        },
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(current_dir, 'css'),
            'tools.staticdir.content_types': {
                'css': 'text/css'
            }
        },
        '/img': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(current_dir, 'img'),
            'tools.staticdir.content_types': {
                'png': 'image/png',
                'png': 'image/jpeg'
            }
        }
    }
    cherrypy.config.update({'server.socket_port': 44444,})
    cherrypy.quickstart(Root(), '/', config=conf)