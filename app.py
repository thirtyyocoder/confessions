from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

#Initialising the database

def init_db():
    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS confessions (id INTEGER PRIMARY KEY, text TEXT, timestamp TEXT)''')
    conn.commit()
    conn.close()


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        confession = request.form['confession']
        conn = sqlite3.connect('confessions.db')
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO confessions (text,timestamp) VALUES (?,?)", (confession,timestamp))
        conn.commit()
        conn.close()
        return redirect('/confessions')
    return render_template('index.html')

@app.route('/confessions')
def show_confessions():
    conn = sqlite3.connect('confessions.db')
    c = conn.cursor()
    c.execute("SELECT text, timestamp FROM confessions ORDER BY id DESC")
    all_confessions = c.fetchall()
    conn.close()
    return render_template('confessions.html',confessions=all_confessions)

if __name__ == '__main__':
    print("Starting Flask app...")
    init_db()
    app.run(debug=True, port=5001)