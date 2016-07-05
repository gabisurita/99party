from app import app
import mapping
import models

wsgi = app.wsgifunc()

if __name__ == "__main__":
  models.createDB()
  app.mapStatic(app.StaticDirs)
  app.run()
