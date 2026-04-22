from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/')
def index():
    conn = get_db()
    citas = conn.execute('SELECT * FROM pacientes ORDER BY fecha').fetchall()
    conn.close()
    return render_template('index.html', citas=citas)

@app.route('/agendar', methods=['GET', 'POST'])
def agendar():
    if request.method == 'POST':
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        with get_db() as conn:
            conn.execute('INSERT INTO pacientes (mascota, propietario, especie, fecha) VALUES (?, ?, ?, ?)',
                         (mascota, propietario, especie, fecha))
        return redirect(url_for('index'))
    return render_template('agendar.html')

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    conn = get_db()
    if request.method == 'POST':
        mascota = request.form['mascota']
        propietario = request.form['propietario']
        especie = request.form['especie']
        fecha = request.form['fecha']
        conn.execute('UPDATE pacientes SET mascota=?, propietario=?, especie=?, fecha=? WHERE id=?',
                     (mascota, propietario, especie, fecha, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    cita = conn.execute('SELECT * FROM pacientes WHERE id = ?', (id,)).fetchone()
    conn.close()
    return render_template('modificar.html', cita=cita)

@app.route('/cancelar/<int:id>')
def cancelar(id):
    with get_db() as conn:
        conn.execute('DELETE FROM pacientes WHERE id = ?', (id,))
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)