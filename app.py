from flask_session import Session
from pymongo import MongoClient
import json
from bson import json_util
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import re
from datetime import datetime

session = []

def connect_to_mongodb(host='languagelearningapp.onj8bnp.mongodb.net', port=27017, username=None, password=None, app_name='LanguageLearningApp'):
    # Construct the connection URI
    uri = f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority&appName={app_name}" 
    # Establish connection to MongoDB
    client = MongoClient(uri)
    return client

client = connect_to_mongodb('languagelearningapp.onj8bnp.mongodb.net', 27017, 'XXXXXXXXXX', 'XXXXXXXXXXXX', 'LanguageLearningApp')
mydb = client["LanguageLearningApp_DB"]

# print(mydb.list_collection_names())

app = Flask(__name__)

# Configure Flask-Session to use server-side sessions
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/api/auth/register', methods=['POST'])
def register_user():
    data = request.json  # Assuming JSON data is sent in the request
    # register_request= {
    #                     "username": "robbin1",
    #                     "email": "robbin1@example.com",
    #                     "password": "robbin_password"
    #                 }
    # Check if required fields are present
    users_collection=mydb['users']
    if 'username' not in data or 'password' not in data:
        print("{'error': 'Username and password are required'}, 400")
        return jsonify({'error': 'Username and password are required'}), 400
    username = data['username']
    password = data['password']
    # Check if username already exists
    if users_collection.find_one({'username': username}):
        print("{'error': 'Username already exists'}, 400")
        return jsonify({'error': 'Username already exists'}), 400
    else:
        # Insert new user into MongoDB
        users_collection.insert_one({'username': username, 'password': password})
        print("{'message': 'User registered successfully'}, 201")
        return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login_user():
    data = request.json  # Assuming JSON data is sent in the request
    # login_request= {
    #                     "username": "robbin1",
    #                     "password": "robbin_password"
    #                 }
    # Check if required fields are present
    users_collection=mydb['users']
    if 'username' not in data or 'password' not in data:
        print("{'error': 'Username and password are required'}, 400")
        return jsonify({'error': 'Username and password are required'}), 400
    username = data['username']
    password = data['password']
    # Query MongoDB for user data
    user = users_collection.find_one({'username': username, 'password': password})
    if not user:
        print("{'error': 'Invalid username or password'}, 401")
        return jsonify({'error': 'Invalid username or password'}), 401
    else:
        # Generate unique session ID for the user
        session.append(username)
        print("{'message': 'Login successful'}, 200")
        return redirect(url_for('get_supported_languages'))
        # return jsonify({'message': 'Login successful'}), 200

@app.route('/api/auth/users', methods=['GET'])
def user_profile():
    # Implementation for getting user profile
    try:
        users_collection=mydb['users']
        users_list = []
        for user in users_collection.find():
            users_list.append({
                'username': user['username'],
                'userid': str(user['_id'])
            })
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": "Opps!! Something went wrong"}), 500

# Language Selection
@app.route('/api/languages', methods=['GET'])
def get_supported_languages():
    # Implementation for getting supported languages
    try:
        languages_collection=mydb['languages']
        languages_list = []
        for document in languages_collection.find():
            languages_list.append({
                'Language': document['name'],
                'Language_Code': document['code']
            })
        return jsonify(languages_list), 200
    except Exception as e:
        return jsonify({"error": "Opps!! Something went wrong"}), 500

@app.route('/api/learning/materials/<string:language_code>', methods=['GET'])
def manage_learning_material(language_code):
    # Implementation for getting/updating/deleting a specific learning material
    try:
        material_collection=mydb['LanguageMaterial']
        material=[]
        query = {"$or": [{"Language": re.compile(language_code, re.IGNORECASE)}, {"LanguageCode": re.compile(language_code, re.IGNORECASE)}]}
        for doc in material_collection.find(query):
            doc = json.loads(json_util.dumps(doc))
            material.append(doc)
        return jsonify("Material: ", material), 200
    except Exception as e:
        return jsonify({"error": "Opps!! Something went wrong"}), 500

@app.route('/api/learning/materials/user_progress/<string:user_name>', methods=['GET'])
def learning_progress(user_name):
    # Implementation for getting specific user's learning progress
    try:
        progress_collection = mydb['LearningProgress']
        progress = []
        print(user_name)
        query = {"username": {"$regex": user_name, "$options": "i"}}
        for doc in progress_collection.find(query):
            doc = json.loads(json_util.dumps(doc))
            progress.append(doc)
        return jsonify({"User_Progress": progress}), 200
    except Exception as e:
        return jsonify({"error": "Opps!! Something went wrong"}), 500

@app.route('/api/learning/materials/user_progress_update/', methods=['POST'])
def learning_progress_update():
    # Implementation for updating specific user's learning progress
    # request_payload= {
    #                     "username": "", -- Required
    #                     "languages": ["English","Hindi"], -- Required
    #                     "lessons": ["Xyz", "Nouns"], -- Required
    #                     "score": 1000, 
    #                     "completed": True/False
    #                 }
    data = request.json
    user_name = data.get('username')
    languages = data.get('languages')
    lessons = data.get('lessons')
    score = data.get('score', 0)
    completed = data.get('completed', False)
    if not user_name or not languages or not lessons:
        return jsonify({'error': 'Incomplete data provided'}), 400
    users_collection=mydb['users']
    user_exists = users_collection.find_one({"username": user_name})    
    if user_exists:
        progress_collection=mydb['LearningProgress']
        puser_exists = progress_collection.find_one({"username": user_name})
        if puser_exists:
            query = {"username": re.compile(user_name, re.IGNORECASE)}
            modified=0
            update_result = progress_collection.update_one(query, {"$addToSet": {"lessons": {"$each": lessons}}})
            modified+=update_result.modified_count
            update_result = progress_collection.update_one(query, {"$addToSet": {"languages": {"$each": languages}}})
            modified+=update_result.modified_count
            if score !=0 :
                update_result = progress_collection.update_one(query, {"$set": {"score": score}})
            if completed:
                update_result = progress_collection.update_one(query, {"$set": {"completed": completed}})
            update_result = progress_collection.update_one(query, {"$set": {"last_updated": datetime.now()}})
            return jsonify({'message': f'User progress updated successfully, modified: {modified}'}), 200
        else:
            progress_data = {
                                "username": user_name,
                                "languages": languages,
                                "lessons": lessons,
                                "completed": completed,
                                "score": score,
                                "last_updated": datetime.now()
                            }
            update_result = progress_collection.insert_one(progress_data)
            return jsonify({'message': f'User progress updated successfully, added: 1'}), 200
    else:
        return jsonify({'message': f'User Not exist '}), 400

@app.route('/api/auth/logout', methods=['POST'])
def logout_user():
    # Assuming you are using Flask session for user authentication
    data = request.json
    username = data['username']
    print(session)
    if username in session:
        session.remove(username)
        return jsonify({'message': 'User logged out successfully'})
    else:
        return jsonify({'error': 'User is not logged in'}), 401

if __name__ == '__main__':
    app.run(debug=True)
