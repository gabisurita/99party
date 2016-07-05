
import web
import os
import codecs
import urllib
import re

from app import *

def postParse(RawPost):
  """Parse POST Filds into dict."""
  FieldList = [Field.split("=") for Field in RawPost.split("&")]

  try:
    FieldMap = {Q[0]: urllib.unquote(Q[1].replace("+", " ")).
                decode('utf8') for Q in FieldList}

    return FieldMap
  except:
      return {}


def isLogged():
  """ Define secure (logged in only) area"""
  try:
    if session.user_id:
      return True
    else:
      return False
  except AttributeError:
    return False


  # Test for custom 404
def notfound():
    return web.notfound(Render.notfound())

try:
    App.notfound = notfound
except:
    pass
