#encoding:utf-8

#TODO Revise login functions in register

import web
import datetime
from app import render, app, session
from models import *
from functions import *


class ToolbarHandler:
  def load(self):
    dbs = sessionmaker(bind=db)()
    
    if "user_id" not in dir(session):
        session.user_id=False
    
    render.user = dbs.query(User).filter(User.id==session.user_id).first()
    render.business = dbs.query(Business).filter(Business.id==session.user_id).first()
    
    render.events = dbs.query(Event)
    render.businesses = dbs.query(Business)
  

class MainController:

  def GET(self):
    ToolbarHandler().load()
    return render.main(None,"",render)


class LoginController:
  
  form = web.form.Form(
    web.form.Textbox('email', web.form.notnull),
    web.form.Password('password', web.form.notnull),
  )

  def GET(self):
    if isLogged():
      raise web.seeother('/')
    
    return render.login(self.form, "", render)

  def POST(self):
    if isLogged():
      raise web.seeother('/')
  
    if not self.form.validates():
      return render.login(self.form, "Todos os campos são obrigatórios.", render)

    dbs = sessionmaker(bind=db)()
    login = dbs.query(Login).filter(Login.email == self.form['email'].value).first()
    
    if login == None:
      return render.login(self.form, "Email não cadastrado", render)
      
    if login.password != self.form['password'].value.encode('base64'):
      return render.login(self.form, "Senha inválida", render)      
      
    if not login.valid:
      return render.login(self.form, "Cadastro sob aprovação.", render)
    
    
    session.user_id = login.id
    
    raise web.seeother('/')


class UserRegisterController:
  
  form = web.form.Form(
    web.form.Textbox('name', web.form.notnull),
    web.form.Textbox('cpf', web.form.notnull),
    web.form.Textbox('tel', web.form.notnull),
    web.form.Textbox('email', web.form.notnull),
    web.form.Password('password', web.form.notnull),
    web.form.Password('confirmation', web.form.notnull),
  )
  
  def GET(self):
    if isLogged():
      raise web.seeother('/')
      
    return render.registerUser(self.form, "", render)

  def POST(self):
    if isLogged():
      raise web.seeother('/')

    if not self.form.validates():
      return render.registerUser(self.form, "Todos os campos são obrigatórios.", render)

    dbs = sessionmaker(bind=db)()
    login = dbs.query(Login).filter(Login.email == self.form['email'].value).first()
    
    if login is not None:
    
      if login.password != self.form['password'].value.encode('base64'):
        return render.login(Form, "Email já cadastrado", render) 
      
      session.user_id = login.id
      raise web.seeother('/')
    
    email = re.search(r'[\w.-]+@[\w.-]', self.form['email'].value)
    cpf = re.search(r'[0-9]{11}', self.form['cpf'].value)
    
    if email is None:
      return Render.register(self.form,"E-mail inválido.", Render)
    if cpf is None:
      return Render.register(self.form,"CPF inválido.", Render)
    
    if self.form['password'].value != self.form['confirmation'].value:
      return Render.register(self.form,"Senhas não correspondem.", Render)
    
    newLogin = Login(
      email = self.form['email'].value,
      password = self.form['password'].value.encode('base64'),
      valid = True
    )
    
    dbs.add(newLogin)
    dbs.commit()
    
    login = dbs.query(Login).filter(Login.email == newLogin.email).first()
    
    newUser = User(
      login = login,
      name = self.form['name'].value,
      cpf = self.form['cpf'].value,
      tel = self.form['tel'].value,
    )
    
    dbs.add(newUser)
    dbs.commit()
    
    session.user_id = login.id
    raise web.seeother('/')


class BusinessRegisterController:

  form = web.form.Form(
    web.form.Textbox('name', web.form.notnull),
    web.form.Textbox('cnpj', web.form.notnull),
    web.form.Textbox('address', web.form.notnull),
    web.form.Textbox('tel', web.form.notnull),
    web.form.Textbox('email', web.form.notnull),
    web.form.Password('password', web.form.notnull),
    web.form.Password('confirmation', web.form.notnull),
  )
  
  def GET(self):
    if isLogged():
      raise web.seeother('/')
      
    return render.registerBusiness(self.form, "", render)

  def POST(self):
    if isLogged():
      raise web.seeother('/')

    if not self.form.validates():
      return render.registerBusiness(self.form, "Todos os campos são obrigatórios.", render)

    dbs = sessionmaker(bind=db)()
    login = dbs.query(Login).filter(Login.email == self.form['email'].value).first()
    
    if login is not None:
    
      if login.password != self.form['password'].value.encode('base64'):
        return render.login(Form, "Email já cadastrado", render) 
      
      if not login.valid:
        return render.login(Form, "Cadastro sob aprovação.", render) 
      
      session.user_id = login.id
      raise web.seeother('/')
    
    email = re.search(r'[\w.-]+@[\w.-]', self.form['email'].value)
    cnpj = re.search(r'[0-9]{14}', self.form['cnpj'].value)
    
    if email is None:
      return Render.register(self.form,"E-mail inválido.", Render)
    if cnpj is None:
      return Render.register(self.form,"CNPJ inválido.", Render)
    
    if self.form['password'].value != self.form['confirmation'].value:
      return Render.register(self.form,"Senhas não correspondem.", Render)
    
   #TODO Turn false
    newLogin = Login(
      email = self.form['email'].value,
      password = self.form['password'].value.encode('base64'),
      valid = True
    )
    
    dbs.add(newLogin)
    dbs.commit()
    
    login = dbs.query(Login).filter(Login.email == newLogin.email).first()
    
    newBusiness = Business(
      login = login,
      name = self.form['name'].value,
      address = self.form['address'].value,
      cnpj = self.form['cnpj'].value,
      tel = self.form['tel'].value,
    )
    
    dbs.add(newBusiness)
    dbs.commit()
    
    session.user_id = login.id
    raise web.seeother('/')


class LogoutController:
  def GET(self):
    session.user_id = False
    raise web.seeother('/')

class EventCreatorController:
  form = web.form.Form(
    web.form.Textbox('name', web.form.notnull),
    web.form.Textbox('date', web.form.notnull),
    web.form.Textbox('location', web.form.notnull),
    web.form.Textbox('description'),
    web.form.Textbox('picture'),
  )
  
  def GET(self):
    ToolbarHandler().load()
    return render.newEvent(form,"",render)
  
  def POST(self):
    dbs = sessionmaker(bind=db)()
    creator = dbs.query(Business).filter(Business.id==session.user_id).first() 
    
    if creator is None:
      raise web.seeother('/')
    
    if not self.form.validates():
      return render.newEvent(self.form, "Todos os campos são obrigatórios.", render)
    
    date = datetime.datetime.strptime(self.form["date"].value, "%m/%d/%Y %I:%M %p")

    newEvent = Event(
      creator = creator,
      name = self.form['name'].value,
      date = date,
      location = self.form['location'].value,
      picture = ""
    )
    
    dbs.add(newEvent)
    dbs.commit()
    raise web.seeother('/')
  
class EventController:
  
  event = Event()
  
  def GET(self):
    ToolbarHandler().load()
    return render.event(self.event,"", render)

class UserController:
  
  user = User()
  
  def GET(self):
    ToolbarHandler().load()
    return render.user(self.user,"", render)


class BusinessController:
  
  business = Business()
  
  def GET(self):
  
    dbs = sessionmaker(bind=db)() 
    self.business.events = dbs.query(Event).filter(Event.creator == self.business)
    
    ToolbarHandler().load()
    return render.businessPage(self.business,"",render)

  
class EventSearchController:
  def GET(self):
    ToolbarHandler().load()
    return "Hi!"


class UploadHandler:
  def GET(self):
    return """
      <form method="POST" enctype="multipart/form-data" action="">
      <input type="file" name="myfile" />
      <br/>
      <input type="submit" />
      </form>
      """

  def POST(self):
    x = web.input(myfile={})
    filedir = 'uploads/' # change this to the directory you want to store the file in.
    
    if 'myfile' in x: # to check if the file-object is created
      filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
      filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
      fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
      fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
      fout.close() # closes the file, upload complete.
    raise web.seeother('/upload')


