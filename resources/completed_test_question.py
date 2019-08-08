from flask_restful import Resource, reqparse
from models.completed_tests_questions import CompletedTestQuestionsModel
from flask import request
from flask import jsonify

class ResponseObj:
  def __init__(self, id, question_name, question_description, ans, correct_answer):
    self.id = id
    self.question_name = question_name
    self.question_description = question_description
    self.answer = ans
    self.correct_answer = correct_answer

  def json(self):
    return {'id': self.id,
            'question_name': self.question_name,
            'question_description': self.question_description,
            'answer': self.answer,
            'correct_answer': self.correct_answer
            }


class CompletedTestQuestionByID(Resource):
  def post(self):
    respArray = []
    data = request.get_json(force=True)
    print(data['id'])
    t= CompletedTestQuestionsModel.query.filter_by(test_id=data['id']).all()
    for q in t:
      resp = ResponseObj(q.id, q.question.name, q.question.description, q.answer, q.correct_answer).json()
      respArray.append(resp)
      print(q.question.description)
    print(t)
    print('asd')
    return (respArray)

