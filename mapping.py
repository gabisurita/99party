from main import *
from models import *

from app import map


map(MainController, "/")
map(LoginController, "/login")
map(LogoutController, "/logout")
map(UserRegisterController, "/registrar")
map(BusinessRegisterController, "/registrar_empresa")
map(EventCreatorController, "/criar_evento")
map(EventSearchController, "/busca")

dbs = sessionmaker(bind=db)()

events = dbs.query(Event)
business = dbs.query(Business)

for el in events:
  map(
    EventController, 
    str("/eventos/%s" % el.name.lower().replace(" ","_").encode('utf8')),
    dict(event=el)
  )

for el in business:
  map(
    BusinessController, 
    str("/empresas/%s" % el.name.lower().replace(" ","_").encode('utf8')),
    dict(business=el)
  )
