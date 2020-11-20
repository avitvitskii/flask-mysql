from flask import Flask, render_template, g, request, redirect, url_for
import mysql.connector
import humanize
import json

app = Flask(__name__)


def get_db():
    if not hasattr(g, 'db'):
        config = {
            'user': 'root',
            'password': 'somepass',
            'host': 'db',
            "port": '3306',
            "database": 'database'
        }
        g.db = mysql.connector.connect(**config)
    return g.db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def show_students():
    cursor = get_db().cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT * FROM students')
    rows = []
    for row in cursor.fetchall():
        rows.append({
            'id': row['id'],
            'name': row['name'],
            'created_at': row['created_at']
        })
    cursor.close()
    return render_template('index.html', rows=rows)


@app.route('/add', methods=["POST"])
def add_post():
    db = get_db()
    cur = db.cursor()
    sql = "INSERT students(name) VALUES (%s)"
    value = (request.form['student'],)
    cur.execute(sql, value)
    db.commit()
    return redirect(url_for('show_students'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
