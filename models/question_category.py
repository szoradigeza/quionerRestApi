from db import db
from sqlalchemy import ForeignKey

class QuestionCategoryModel(db.Model):
  __tablename__ = 'question_category'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50), index=True)

  def json(self):
    return { 'id': self.id, 'name': self.name }

  def flush_db(self):
    db.session.add(self)
    db.session.flush()

  def save_to_db(self):
    db.session.commit()
    db.session.close()
