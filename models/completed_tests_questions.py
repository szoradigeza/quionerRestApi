from db import db
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
class CompletedTestQuestionsModel(db.Model):
  __tablename__='completed_tests_questions'
  id=db.Column(db.Integer,primary_key=True)
  test_id=db.Column(db.Integer)
  question_id=db.Column(db.Integer, ForeignKey("questions.id"))
  answer=db.Column(db.String(255))
  correct_answer = db.Column(db.String(255))
  question = relationship("QuestionModel")

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
    db.session.close()

