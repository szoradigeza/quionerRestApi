from db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class AnswersModel(db.Model):
  __tablename__='answers'
  id=db.Column(db.Integer,primary_key=True)
  question_id=db.Column(db.Integer, ForeignKey("questions.id"))
  correct = db.Column(db.Integer)
  answer=db.Column(db.String(255))
  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
    db.session.close()

  def serialize_answers(self):
    return {
      'id': self.id,
      'question_id': self.question_id,
      'answer': self.answer,
      'correct': self.correct
    }
  def serialize_answers_without_correct(self):
    return {
      'id': self.id,
      'question_id': self.question_id,
      'answer': self.answer
    }
  @classmethod
  def getCorrectAnswer(cls, id):
    return cls.query.filter_by(question_id=id).filter_by(correct=1).first()
