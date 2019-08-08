from flask_restful import Resource, reqparse
from models.answers import AnswersModel
from flask import jsonify
from flask import request
from sqlalchemy.sql.expression import func
from models.question import QuestionModel
from models.tests import TestModel
from models.test_question import Test_QuestionModel
parser = reqparse.RequestParser()
from models.completed_tests import CompletedTestModel
from models.completed_tests_questions import CompletedTestQuestionsModel
from flask_jwt_extended import (jwt_required)
parser = reqparse.RequestParser()
from models.question_category import QuestionCategoryModel
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
class TestGeneration(Resource):

  def getRandQuestion(self, categoryID, diff, difNum):
    return list(map(lambda x: x.serialize_QuestionModel(),
             QuestionModel.query.filter_by(difficulty=diff).filter_by(category_id=categoryID).order_by(func.random()).limit(difNum)))

  def post(self):
    """data = request.get_json(force=True)
    difNum1 = data['difficulty1']
    difNum2 = data['difficulty2']
    difNum3 = data['difficulty3']
    difNum4 = data['difficulty4']
    difNum5 = data['difficulty5']
    dif1 = self.getquery(1, difNum1)
    dif2 = self.getquery(2, difNum2)
    dif3 = self.getquery(3, difNum3)
    dif4 = self.getquery(4, difNum4)
    dif5 = self.getquery(5, difNum5)
    sum = dif1 + dif2 + dif3 + dif4 + dif5"""
    try:
      data = request.get_json(force=True)
      print(data)
      questions = []
      for categoryData in data:
        difficulties = categoryData['difficulties']
        for i in range(len(difficulties)):
          print(categoryData['categoryID'], i+1, difficulties[i])
          asd = self.getRandQuestion(categoryData['categoryID'], i+1, difficulties[i])
          print(asd)
          if len(asd):
            questions += asd
      print(questions)
    except NameError:
      print(NameError)
    return questions

class CreateOnlineTest(Resource):
  def post(self):
    data = request.get_json(force=True)
    new_test = TestModel(
      test_writer_name=data['name'],
      start_date=data['start_date'],
      end_date=data['end_date'],
      time=data['time']
    )
    #new_test_commit=new_test
    new_test.flush_db()

    #print(new_test.id)
    questionIDs=data['question_id']
    testid = new_test.id
    #print(questionIDs)
    new_test.save_to_db()
    for q in questionIDs:
      new_testQuestion = Test_QuestionModel(
      test_id=testid,
      quest_id=q
      )
      new_testQuestion.save_to_db()
    return {'ok': 'ok'}

class ActiveTest(Resource):
  def get(self):
    print('active Test')
    return list(map(lambda x: x.json(), TestModel.query.all()))

class getTestbyID(Resource):
  def post(self):
    data = request.get_json(force=True)
    dataId = data['id']
    tests = Test_QuestionModel.query.filter_by(test_id=dataId).all()
    print(tests)
    testRespSum = []
    for test in tests:
      answers = []
      for ans in test.question.answers:
        answers.append(ans.serialize_answers_without_correct())
      testResp = {
        'questionId': test.question.id,
        'description': test.question.description,
        'answers': answers
      }
      testRespSum.append(testResp)
      print(testRespSum)
    return jsonify(testRespSum)

class sendtestResult(Resource):
  def post(self):
    data = request.get_json(force=True)
    print(data)
    response = []
    questionCounter = 0
    point = 0
    for question in data['testdata']:
      correctAns=AnswersModel.getCorrectAnswer(question['question_id'])
      questionCounter += 1
      questionData = {
        'question_id': correctAns.question_id,
        'answer': correctAns.answer
      }
      newCompletedTest = CompletedTestQuestionsModel(
        test_id=data['testid'],
        question_id=correctAns.question_id,
        answer=question['answer'],
        correct_answer=correctAns.answer
      )
      if question['answer'] == correctAns.answer:
        point += 1
      response.append(questionData)
      newCompletedTest.save_to_db()
    print(response, questionCounter, point)
    newCompletedTest =  CompletedTestModel(
      test_writer_name=data['testwriter'],
      test_id=data['testid'],
      question_num=questionCounter,
      correct_answer_num=point,
      fill_time = data['date'])
    updateTestModel = TestModel.find_by_id(data['testid'])
    updateTestModel.completed=1
    updateTestModel.save_to_db()
    newCompletedTest.save_to_db()
    return {'maxpoint': questionCounter,
            'userpoint': point,
            'correctAns': response}

class getTests(Resource):
  @jwt_required
  def get(self):
    print('leker')
    return list(map(lambda x: x.json(), CompletedTestModel.query.all()))
