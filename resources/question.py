from flask_restful import Resource, reqparse
from models.question import QuestionModel
from models.answers import AnswersModel
from flask import jsonify
from flask import request
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required)
from models.question_category import QuestionCategoryModel

class Question(Resource):
  def get(self, questionName):
    question = QuestionModel.find_by_name(questionName)
    if question:
      return question.json()
    return {'message': 'Item not found'}, 404


class getAllQuestion(Resource):
    def get(self):
        return list(map(lambda x: x.json(), QuestionModel.query.all()))

class addQuestion(Resource):
  @jwt_required
  def post(self):
    try:
      counter = 0
      data = request.get_json(force=True)
      #print(data)
      num =int(data['correctAnswerNum'])
      new_question = QuestionModel(
        name= data['name'],
        description= data['description'],
        difficulty= data['difficulty'],
        category_id= data['category_id']
      )
      new_question.flush_db()
      questionId = new_question.id
      new_question.save_to_db()
      data = data['answers']
      #print(questionId)
      for answer in data:
        if counter == num:
          new_answer = AnswersModel(
            question_id=questionId,
            answer=answer,
            correct='1'
          )
        else:
            new_answer = AnswersModel(
              question_id=questionId,
              answer=answer,
              correct='0'
            )
        new_answer.save_to_db()
        counter += 1
      return {'response': 'Succesfull' },200
    except Exception as e:
      print('ez a hiba', e)
      return {'response': 'Invalid data' }, 400

class editQuestion(Resource):
  def post(self):
      data = request.get_json(force=True)
      #print(data['question_id'])
      #QuestionModel.query.filter_by(id=data['question_id']).delete()
      #QuestionModel.save_to_db(self)
      #AnswersModel.query.filter_by(question_id=data['question_id']).delete()
      return {'response': 'Succesfull' },200


class diffByNum(Resource):
  def post(self):
    data = request.get_json(force=True)['categoryIDs']
    print(data)
    data.sort()
    print(data)
    numberArray = []
    resp = []
    for id in data:
      for diff in range(1,6):
        #print(diff)
        number = QuestionModel.difficultyByNumber(diff, id)
        numberArray.append(number)
      #print(numberArray)
      categoryName = QuestionCategoryModel.query.filter_by(id=id).first().name
      #print(categoryName)
      resp.append({
        'category_id': id,
        'category_name': categoryName,
        'numberOfQuestion': numberArray
      })
      numberArray = []
    #print(resp)
    return (resp)
#    return {'difficulty1': num1, 'difficulty2': num2, 'difficulty3': num3, 'difficulty4': num4, 'difficulty5': num5}
class getQuestionCategories(Resource):
  def get(self):
    return list(map(lambda x: x.json(), QuestionCategoryModel.query.all()))

class createNewQuestionCategory(Resource):
  def post(self):
    categoryname=request.get_json(force=True)['categoryname']
    existname=QuestionCategoryModel.query.filter_by(name=categoryname).first()
    print(existname)
    if existname is not None:
        return{'message': 'exist'}, 200
    else:
        newCategory = QuestionCategoryModel(name=categoryname)
        newCategory.flush_db()
        id = newCategory.id
        newCategory.save_to_db()
        return {'message': id},200

