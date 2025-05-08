from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In-memory storage for students
students = []
student_id_counter = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    global student_id_counter
    if request.method == 'POST':
        data = request.json
        student = {
            'ID': student_id_counter,
            'name': data['name'],
            'email': data['email'],
            'age': data['age'],
            'grade': data['grade'],
            'degree': data['degree']
        }
        students.append(student)
        student_id_counter += 1
        return jsonify({'message': 'Student added successfully!'})
    else:
        return jsonify(students)

@app.route('/students/<int:id>', methods=['PUT', 'DELETE'])
def update_delete_student(id):
    if request.method == 'PUT':
        data = request.json
        for student in students:
            if student['ID'] == id:
                student.update(data)
                return jsonify({'message': 'Student updated successfully!'})
        return jsonify({'message': 'Student not found'}), 404

    elif request.method == 'DELETE':
        global students
        students = [s for s in students if s['ID'] != id]
        return jsonify({'message': 'Student deleted successfully!'})

@app.route('/search')
def search_student():
    query = request.args.get('q', '').lower()
    results = [s for s in students if query in s['name'].lower() or query in s['email'].lower() or query in s['degree'].lower()]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
