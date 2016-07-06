from main import *
from models import *

from app import map


map(MainController, "/")
map(LoginController, "/login")
map(LogoutController, "/logout")
map(UserRegisterController, "/registrar")
map(BusinessRegisterController, "/registrar_empresa")
map(EventCreatorController, "/criar_evento")
map(SearchController, "/busca")

dbs = sessionmaker(bind=db)()

events = dbs.query(Event)
business = dbs.query(Business)

for el in events:
  map(
    EventController, 
    el.urlEncode(),
    dict(event=el)
  )
  
  map(
    EventConfirmationHandler, 
    el.urlEncode()+"/participar",
    dict(event=el)
  )
  
  map(
    UserConfirmationHandler, 
    el.urlEncode()+"/confirmar",
    dict(event=el)
  )

for el in business:
  map(
    BusinessController, 
    el.urlEncode(),
    dict(business=el)
  )
