from db import db

class CompletedTestModel(db.Model):
  __tablename__='completed_tests'
  id=db.Column(db.Integer,primary_key=True)
  test_writer_name=db.Column(db.String(50))
  test_id = db.Column(db.Integer)
  question_num=db.Column(db.Integer)
  correct_answer_num = db.Column(db.Integer)
  fill_time = db.Column(db.String(50))

  def save_to_db(self):
    db.session.add(self)
    db.session.commit()
    db.session.close()

  def json(self):
    return {
      'id': self.id,
      'test_writer_name': self.test_writer_name,
      'test_id': self.test_id,
      'question_num': self.question_num,
      'correct_answer_num': self.correct_answer_num,
      'fill_time': self.fill_time
    }
