from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask App
app = Flask(__name__)

# Configure SQLite Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database Plugin
db = SQLAlchemy(app)

# Database Model (Defines the 'Task' Table Structure)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

# Create Database File & Table automatically
with app.app_context():
    db.create_all()

# Route 1: Display Tasks & Add New Task
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        if task_content:
            new_task = Task(title=task_content)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))

    # Fetch all tasks from the database
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# Route 2: Delete a Task by ID
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)