from flask import Flask, g, render_template, request
import sqlite3

app = Flask(__name__)

@app.before_request
def before_request():
    g.db = sqlite3.connect("emails.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/signup', methods = ['POST'])
def signup():
    email = request.form['email']
    g.db.execute("INSERT INTO email_addresses VALUES (?)", [email])
    g.db.commit()
    return redirect('/')

@app.route('/emails')
def emails():
    email_addresses = g.db.execute("SELECT email FROM email_addresses").fetchall()
    return render_template('emails.html', email_addresses=email_addresses)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
