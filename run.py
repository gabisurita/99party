import app
import mapping
import models

if __name__ == "__main__":
  models.createDB()
  app.mapStatic(app.StaticDirs)
  app.app.run()
