from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'citas.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mascota TEXT NOT NULL,
                propietario TEXT NOT NULL,
                especie TEXT,
                fecha TEXT NOT NULL
            )
        ''')
    print("Base de datos inicializada")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)