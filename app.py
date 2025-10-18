from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection (use local MongoDB if env variable is not set)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["student_db"]
students_collection = db["students"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/students', methods=['GET'])
def get_students():
    students = []
    for student in students_collection.find():
        student['_id'] = str(student['_id'])  # Convert ObjectId to string for JSON serialization
        students.append(student)
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    grade = data.get('grade')

    if name and age and grade:
        try:
            age = int(age)
        except ValueError:
            return jsonify({'error': 'Age must be a number'}), 400

        new_student = {'name': name, 'age': age, 'grade': grade}
        result = students_collection.insert_one(new_student)
        return jsonify({'message': 'Student added', 'id': str(result.inserted_id)}), 201

    return jsonify({'error': 'Invalid data'}), 400

@app.route('/api/students/<id>', methods=['DELETE'])
def delete_student(id):
    try:
        result = students_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Student deleted'}), 200
        return jsonify({'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Invalid student ID format: {str(e)}'}), 400

if __name__ == '__main__':
    app.run(debug=True)
