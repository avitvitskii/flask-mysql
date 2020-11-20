from flask import Flask, render_template, g, request, redirect, url_for
import mysql.connector
import humanize
import json

app = Flask(__name__)


# def get_db():
#     if not hasattr(g, 'db'):
#         config = {
#             'user': 'root',
#             'password': 'somepass',
#             'host': 'db',
#             "port": '3306',
#             "database": 'database'
#         }
#         g.db = mysql.connector.connect(**config)
#     return g.db


# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'db'):
#         g.db.close()


@app.route('/')
def hello_world():
    config = {
        'user': 'root',
        'password': 'somepass',
        'host': 'db',
        "port": '3306',
        "database": 'database'
    }
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor(buffered=True, dictionary=True)
    cursor.execute('SELECT * FROM students')
    rows = []
    for row in cursor.fetchall():
        rows.append({
            'id': row['id'],
            'name': row['name'],
            'created_at': humanize.naturaltime(row['created_at'])
        })
    cursor.close()
    connection.close()
    return render_template('index.html', rows=rows)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
