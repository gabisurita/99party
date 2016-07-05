from app import app
import mapping
import models

if __name__ == "__main__":
  models.createDB()
  app.run()
