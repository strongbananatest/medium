from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db():
    db = sqlite3.connect('todos.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with get_db() as db:
        db.execute('CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT NOT NULL)')

init_db()

@app.route('/')
def index():
    db = get_db()
    todos = db.execute('SELECT id, task FROM todos').fetchall()
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    todo = request.form.get('todo')
    if todo:
        db = get_db()
        db.execute('INSERT INTO todos (task) VALUES (?)', (todo,))
        db.commit()
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    db = get_db()
    db.execute('DELETE FROM todos WHERE id = ?', (id,))
    db.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)