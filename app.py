from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# In-memory store for demo (replace with DB for production)
students = [
    {"id": 1, "name": "Alice", "branch": "CSE", "year": "3"},
    {"id": 2, "name": "Bob", "branch": "IT", "year": "2"},
    {"id": 3, "name": "Sindhuja", "branch": "IT", "year": "4"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def list_students():
    return render_template('students.html', students=students)

@app.route('/add-student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    branch = request.form.get('branch')
    year = request.form.get('year')
    if name:
        new_id = max([s['id'] for s in students]) + 1 if students else 1
        students.append({"id": new_id, "name": name, "branch": branch, "year": year})
    return redirect(url_for('list_students'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
