from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('register.html')

# Registration route
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    
    # Save to SQLite database
    conn = sqlite3.connect('mydatabase.db')  # Updated database name
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                   (username, password, first_name, last_name, email))
    conn.commit()
    conn.close()

    return redirect(url_for('welcome', first_name=first_name, last_name=last_name, email=email))

# Welcome route
@app.route('/welcome')
def welcome():
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    email = request.args.get('email') 
    return render_template('welcome.html', first_name=first_name, last_name=last_name, email=email)

# Login route
@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
 
    # Check the user in SQLite database
    conn = sqlite3.connect('mydatabase.db')  # Updated database name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Successful login
        return f"""
            <h1>Welcome back!!!</h1>
            <h2>Email: {user[3]}<h2>
            <h2>First Name: {user[4]}<h2>
            <h2>Last Name: {user[5]}<h3>
            <p>Your login was successful.</p>
            <a href="/"><button>Register</button></a>
            <a href="/login"><button>Logout</button></a>
        """  # Buttons to go back to register and login pages
    else:
        # Incorrect credentials
        return f"""
            <h1>Invalid username or password. Please try again.</h1>
            <a href="/"><button>Register</button></a>
            <a href="/login"><button>Login</button></a>
        """  # Buttons to go back to register and login pages


if __name__ == '__main__':
    app.run(debug=True)