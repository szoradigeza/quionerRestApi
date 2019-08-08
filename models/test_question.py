from db import db
from sqlalchemy.orm import relationship
from models.question import QuestionModel
from sqlalchemy import ForeignKey

class Test_QuestionModel(db.Model):
  __tablename__='test_questions'
  id=db.Column(db.Integer,primary_key=True)
  test_id=db.Column(db.Integer)
  quest_id=db.Column(db.Integer, ForeignKey("questions.id"))
  question = relationship("QuestionModel")

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
    db.session.close()
  @classmethod
  def getbytestID(cls, testID):
    cls.query.filter_by(test_id=testID).all()

