from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from resources.User import *
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from resources.question import *
from sqlalchemy.orm import scoped_session, sessionmaker
import pymysql
from resources.test import *
from models.user import RevokedTokenModel
from flask_socketio import SocketIO, emit
from resources.completed_test_question import CompletedTestQuestionByID
pymysql.install_as_MySQLdb()




app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adminuser:kuplung@localhost:3306/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['SQLALCHEMY_POOL_SIZE'] = 100
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30



db = SQLAlchemy(app)
api = Api(app)
socketio = SocketIO(app)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db))

@app.teardown_appcontext
def shutdown_session(exception=None):
  db.session.remove()

@socketio.on('message')
def handle_my_custom_event(data):
    print('Connected')
    emit('message', data, broadcast=True)

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('message')
def handle_message(message):
    emit('message', message, broadcast=True)


@socketio.on('connect')
def test_connect():
  emit('my response', {'data': 'Connected'})
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)

#Users
api.add_resource(UserRegistration, '/registration')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
api.add_resource(AllUsers, '/users')


#Token
api.add_resource(TokenRefresh, '/token/refresh')

#question
api.add_resource(diffByNum, '/question/difbynum')
api.add_resource(TestGeneration, '/question/testgen')
api.add_resource(editQuestion, '/question/editquestion')
api.add_resource(getQuestionCategories, '/question/questioncategories')
api.add_resource(addQuestion, '/question/addquestion')
api.add_resource(createNewQuestionCategory, '/question/newcategory')

#Test
api.add_resource(CreateOnlineTest, '/test/createtest')
api.add_resource(ActiveTest, '/test/getactivetest')
api.add_resource(getAllQuestion, '/question/getquestions')
api.add_resource(getTestbyID, '/test/testbyid')
api.add_resource(sendtestResult, '/test/testresult')
api.add_resource(getTests, '/test/alltest')
api.add_resource(CompletedTestQuestionByID, '/test/completedtestbyid')

if __name__ == '__main__':
    db.init_app(app)
    socketio.run(app, port=5000)

