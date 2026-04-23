from flask import Flask, render_template, request, redirect, session
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = "secretkey123"

# Create database
def init_db():
    conn = sqlite3.connect("users.db")
    conn.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect('/login')

# Register
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.hashpw(request.form['password'].encode(), bcrypt.gensalt())

        conn = sqlite3.connect("users.db")
        conn.execute("INSERT INTO users VALUES (?,?)", (username, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("users.db")
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode(), user[1]):
            session['user'] = username
            return redirect('/dashboard')

    return render_template('login.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', user=session['user'])
    return redirect('/login')

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)
