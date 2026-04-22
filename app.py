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
        
        ejemplo = [
            ("Luna", "Marcos Valencia", "Perro", "2025-04-25 10:00"),
            ("Misi", "Fernando Tonconi", "Gato", "2025-04-26 14:30"),
            ("Piolin", "Ana Valencia", "Ave", "2025-04-27 09:15")
        ]
        for m,p,e,f in ejemplo:
            conn.execute('INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?,?,?,?)',
                         (m,p,e,f))
    
    print("Base de datos inicializada con datos de ejemplo")

@app.route('/')
def index():
    conn = get_db()
    citas = conn.execute('SELECT * FROM pacientes ORDER BY fecha').fetchall()
    conn.close()
    return render_template('index.html', citas=citas)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)