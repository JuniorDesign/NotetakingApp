from scribe import db
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from scribe.model.user import User
from scribe.repositories.userRepository import UserRepository



class HelloWorld(Resource):
	def get(self): #example of api
		return "hello world!"

class GetPassword(Resource):
	def __init__(self):
		self.userRepository = UserRepository()
	def get(self):
		user = self.userRepository.find(1);
		return user.as_dict();

class UserRegistration(Resource):
	def __init__(self):
		self.reqparse = RequestParser() #this parses the JSON files that get posted via ajax
		self.reqparse.add_argument('username', type=str, required= True, help="GaTech Username is required to register", location='json')
		self.reqparse.add_argument('password', type=str, required= True, help="Password is required to register", location='json')
		self.reqparse.add_argument('firstName', type=str, required= True, help="First name is required to register", location='json')
		self.reqparse.add_argument('lastName', type=str, required= True, help="Last name is required to register", location='json')
		self.reqparse.add_argument('type', type=str, required= True, help="Type is required to register", location='json')
		super(UserRegistration, self).__init__()

	def post(self): 
		args = self.reqparse.parse_args()
		#Taking the information from the registration form and assinging it to Python variables
		username = args['username']
		password = args['password']
		firstName = args['firstName']
		lastName = args['lastName']
		approved = True #approve users by default at this point

		if args['type'] == "admin":
			accountType = "ADMIN"
		elif args['type'] == "requester":
			accountType = "REQUESTER"
		elif args['type'] == "taker":
			accountType = "TAKER"
		else: #this is how you set a response json and a response status code
			return {"error": "Account type is missing"}, 400

		#once we have a working db here, first check if the user exists or not
		#currently assuming all users are brand new
		userRepository = UserRepository()
		newUser = User(username, password, firstName, lastName, accountType, approved)
		userRepository.add_or_update(newUser)
		userRepository.save_changes()
		print("user has been added to the db!")

		return {"message": "Post to database was successful. New user registered."}
		#if not userRepository.user_exists(user['email']):
          #	new_user = User(uid, user['first_name'], user['last_name'], user['email'])
           #     user_repository.add_or_update(new_user)
		#	user_repository.save_changes()


