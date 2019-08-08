from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt)
from models.user import UserModel, RevokedTokenModel
from models.user_rights import UserRightsModel
from flask import request
parser = reqparse.RequestParser()
parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)
import jwt
import datetime

class UserRegistration(Resource):
  def post(self):
    parser.add_argument('rights', help='This field cannot be blank', required=True)
    data = parser.parse_args()
    if UserModel.find_by_username(data['username']):
      return {'message': 'User {} already exists'.format(data['username'])}
    new_user = UserModel(
      username=data['username'],
      password_hash=UserModel.generate_hash(data['password']),
      rights=data['rights']
    )
    try:
      new_user.save_to_db()
      access_token = create_access_token(identity=data['username'])
      refresh_token = create_refresh_token(identity=data['username'])
      return {
        'message': 'User {} was created'.format(data['username']),
        'access_token': access_token,
        'refresh_token': refresh_token
      }
    except Exception as e:
      return {'message:': 'Something went wrong{}'.format(e)}, 500


class UserLogin(Resource):
  def post(self):
    data = parser.parse_args()
    current_user = UserModel.find_by_username(data['username'])
    if not current_user:
      return {'message': 'Wrong credentials'},403

    if UserModel.verify_hash(data['password'], current_user.password_hash):
      token = {
        'username': data['username'],
        'role': UserRightsModel.getUserRight(current_user.rights)
      }
      expires = datetime.timedelta(days=1)
      access_token = create_access_token(identity=token, expires_delta=expires)
      refresh_token = create_refresh_token(identity=token)

      return {
        'idToken': access_token,
        'refresh_token': refresh_token
      }
    else:
      return {'message': 'Wrong credentials'},403


class UserLogoutAccess(Resource):
  @jwt_required
  def post(self):
    jti = get_raw_jwt()['jti']
    try:
      revoked_token = RevokedTokenModel(jti=jti)
      revoked_token.add()
      return {'message': 'Access token has been revoked'}
    except Exception as e:
      return {'message': 'Something went wrong {}'.format(e)}, 500


class UserLogoutRefresh(Resource):
  @jwt_refresh_token_required
  def post(self):
    jti = get_raw_jwt()['jti']
    try:
      revoked_token = RevokedTokenModel(jti=jti)
      revoked_token.add()
      return {'message': 'Refresh token has been revoked'}
    except:
      return {'message': 'Something went wrong'}, 500


class TokenRefresh(Resource):
  def post(self):
    print('token Refresh!!!!')
    encoded_jwt = request.get_json(force=True)['refresh_token']
    print(jwt.decode(encoded_jwt, 'jwt-secret-string', algorithms=['HS256']))
    decoded = jwt.decode(encoded_jwt, 'jwt-secret-string', algorithms=['HS256'])['identity']
    username = decoded['username']
    token = {
      'username': username,
      'role': decoded['role']
    }
    print(token)
    new_token = create_access_token(identity=token)
    ret = {'access_token': new_token}
    return ret, 200


class AllUsers(Resource):
  def get(self):
    return UserModel.return_all()

  def delete(self):
    return UserModel.delete_all()


class SecretResource(Resource):
  @jwt_required
  def get(self):
    return {
      'answer': 42
    }
