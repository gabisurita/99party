"""99Party Website."""

from __future__ import division


import web
import os
import codecs
import urllib
import re


BaseDir = "."
BaseTitle = "99 Party"
StaticDirs = ["static"]

# Initialize mailing features
web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = '99partyadm@gmail.com'
web.config.smtp_password = '99gudwin'
web.config.smtp_starttls = True

# Render the layouts
render = web.template.render(BaseDir+'/views/',cache=False, globals=globals())


# initialize the application
app = web.application(mapping=(), fvars=globals())

# User session accounts handled by file
session = web.session.Session(app, web.session.DiskStore(
    'sessions'), initializer={})

web.config.debug = False

def map(Inst, URL, attMap={}):
  """ Map an object to an URL. """

  globals()[URL] = type(URL, (Inst, object,), attMap)
  app.add_mapping(URL.lower().replace(
      " ", "_").decode("utf8"), URL)
  app.add_mapping(URL.lower().replace(
      " ", "_").decode("utf8")+"/", URL)


def mapStatic(staticDirs):
    for d in staticDirs:
      try:
        path = os.path.abspath(__file__) + "/" + d
        app.add_mapping("%s/.+" % d, path)
      except AttributeError:
        pass

  # Test for custom 404
#def notfound():
#    return web.notfound(render.notfound())

#try:
#    app.notfound = notfound
#except:
#    pass


